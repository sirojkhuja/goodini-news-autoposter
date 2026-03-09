#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys


def decode_b64(value: str | None) -> str:
    if not value:
        return ""
    return value


def run_psql(sql: str, variables: dict[str, str]) -> str:
    env = os.environ.copy()
    env["PGPASSWORD"] = env["POSTGRES_PASSWORD"]

    cmd = [
        "psql",
        "-h",
        "postgres",
        "-U",
        env["POSTGRES_USER"],
        "-d",
        env["POSTGRES_DB"],
        "-X",
        "-A",
        "-t",
        "-q",
        "-v",
        "ON_ERROR_STOP=1",
    ]

    for key, value in variables.items():
        cmd.extend(["-v", f"{key}={value}"])

    result = subprocess.run(
        cmd,
        input=sql,
        text=True,
        capture_output=True,
        env=env,
        check=True,
    )
    return result.stdout.strip()


def check_duplicate(args: argparse.Namespace) -> int:
    sql = """
SELECT json_build_object(
  'exists',
  EXISTS (
    SELECT 1
    FROM news_posts
    WHERE source_url = convert_from(decode(:'source_url_b64', 'base64'), 'UTF8')
  )
)::text;
"""
    print(run_psql(sql, {"source_url_b64": decode_b64(args.source_url_b64)}))
    return 0


def insert_post(args: argparse.Namespace) -> int:
    sql = """
INSERT INTO news_posts (
  source_url,
  transcript,
  post_text,
  status,
  created_at
) VALUES (
  convert_from(decode(:'source_url_b64', 'base64'), 'UTF8'),
  NULLIF(convert_from(decode(:'transcript_b64', 'base64'), 'UTF8'), ''),
  NULLIF(convert_from(decode(:'post_text_b64', 'base64'), 'UTF8'), ''),
  :'status',
  NOW()
)
RETURNING json_build_object(
  'id', id,
  'source_url', source_url,
  'status', status
)::text;
"""
    print(
        run_psql(
            sql,
            {
                "source_url_b64": decode_b64(args.source_url_b64),
                "transcript_b64": decode_b64(args.transcript_b64),
                "post_text_b64": decode_b64(args.post_text_b64),
                "status": args.status,
            },
        )
    )
    return 0


def update_post_status(args: argparse.Namespace) -> int:
    sql = """
UPDATE news_posts
SET status = :'status'
WHERE id = :'post_id'
RETURNING json_build_object(
  'id', id,
  'source_url', source_url,
  'status', status
)::text;
"""
    print(run_psql(sql, {"post_id": str(args.post_id), "status": args.status}))
    return 0


def log_error(args: argparse.Namespace) -> int:
    sql = """
INSERT INTO error_logs (
  node_name,
  error_message,
  input_data,
  created_at
) VALUES (
  NULLIF(:'node_name', ''),
  convert_from(decode(:'error_message_b64', 'base64'), 'UTF8'),
  CASE
    WHEN :'input_data_b64' = '' THEN NULL
    ELSE convert_from(decode(:'input_data_b64', 'base64'), 'UTF8')::jsonb
  END,
  NOW()
)
RETURNING json_build_object(
  'id', id,
  'node_name', node_name
)::text;
"""
    print(
        run_psql(
            sql,
            {
                "node_name": args.node_name,
                "error_message_b64": decode_b64(args.error_message_b64),
                "input_data_b64": decode_b64(args.input_data_b64),
            },
        )
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check-duplicate")
    check_parser.add_argument("--source-url-b64", required=True)
    check_parser.set_defaults(func=check_duplicate)

    insert_parser = subparsers.add_parser("insert-post")
    insert_parser.add_argument("--source-url-b64", required=True)
    insert_parser.add_argument("--transcript-b64", required=True)
    insert_parser.add_argument("--post-text-b64", required=True)
    insert_parser.add_argument("--status", required=True)
    insert_parser.set_defaults(func=insert_post)

    update_parser = subparsers.add_parser("update-post-status")
    update_parser.add_argument("--post-id", required=True, type=int)
    update_parser.add_argument("--status", required=True)
    update_parser.set_defaults(func=update_post_status)

    log_parser = subparsers.add_parser("log-error")
    log_parser.add_argument("--node-name", required=True)
    log_parser.add_argument("--error-message-b64", required=True)
    log_parser.add_argument("--input-data-b64", default="")
    log_parser.set_defaults(func=log_error)

    return parser


def main() -> int:
    fallbacks = {
        "POSTGRES_USER": "DB_POSTGRESDB_USER",
        "POSTGRES_PASSWORD": "DB_POSTGRESDB_PASSWORD",
        "POSTGRES_DB": "DB_POSTGRESDB_DATABASE",
    }
    for primary, fallback in fallbacks.items():
        if not os.environ.get(primary) and os.environ.get(fallback):
            os.environ[primary] = os.environ[fallback]

    for env_name in ("POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB"):
        if not os.environ.get(env_name):
            print(f"missing required environment variable: {env_name}", file=sys.stderr)
            return 1

    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
