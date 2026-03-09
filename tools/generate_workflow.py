#!/usr/bin/env python3
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
WORKFLOW_PATH = ROOT / "Workflow.json"


def connection(node: str, index: int = 0) -> dict:
    return {"node": node, "type": "main", "index": index}


def if_node(node_id: str, name: str, left_value: str, operator: dict, right_value="", position=None):
    return {
        "parameters": {
            "conditions": {
                "options": {
                    "caseSensitive": True,
                    "leftValue": "",
                    "typeValidation": "strict",
                    "version": 2,
                },
                "conditions": [
                    {
                        "id": f"{node_id}-condition",
                        "leftValue": left_value,
                        "rightValue": right_value,
                        "operator": operator,
                    }
                ],
                "combinator": "and",
            },
            "options": {},
        },
        "id": node_id,
        "name": name,
        "type": "n8n-nodes-base.if",
        "typeVersion": 2.2,
        "position": position or [0, 0],
    }


def respond_node(node_id: str, name: str, response_body: str, response_code: int | str, position=None):
    return {
        "parameters": {
            "respondWith": "json",
            "responseBody": response_body,
            "options": {
                "responseCode": response_code,
            },
        },
        "id": node_id,
        "name": name,
        "type": "n8n-nodes-base.respondToWebhook",
        "typeVersion": 1.1,
        "position": position or [0, 0],
    }


def wait_node(node_id: str, seconds: int, position=None, webhook_id=None):
    return {
        "parameters": {
            "amount": seconds,
            "unit": "seconds",
        },
        "id": node_id,
        "name": f"Wait {seconds}s",
        "type": "n8n-nodes-base.wait",
        "typeVersion": 1,
        "position": position or [0, 0],
        "webhookId": webhook_id or node_id,
    }


def code_node(node_id: str, name: str, js_code: str, position=None, on_error=None):
    node = {
        "parameters": {
            "mode": "runOnceForEachItem",
            "jsCode": js_code,
        },
        "id": node_id,
        "name": name,
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": position or [0, 0],
    }
    if on_error:
        node["onError"] = on_error
    return node


def execute_command_node(node_id: str, name: str, command: str, position=None, on_error=None):
    node = {
        "parameters": {
            "executeOnce": False,
            "command": command,
        },
        "id": node_id,
        "name": name,
        "type": "n8n-nodes-base.executeCommand",
        "typeVersion": 1,
        "position": position or [0, 0],
    }
    if on_error:
        node["onError"] = on_error
    return node


def http_json_node(node_id: str, name: str, url: str, json_body: str, position=None, on_error=None):
    node = {
        "parameters": {
            "method": "POST",
            "url": url,
            "sendHeaders": True,
            "headerParameters": {
                "parameters": [
                    {
                        "name": "Authorization",
                        "value": "=Bearer {{ $env.OPENAI_API_KEY }}",
                    }
                ]
            },
            "sendBody": True,
            "specifyBody": "json",
            "jsonBody": json_body,
            "options": {
                "timeout": 180000,
            },
        },
        "id": node_id,
        "name": name,
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": position or [0, 0],
    }
    if on_error:
        node["onError"] = on_error
    return node


def telegram_node(node_id: str, name: str, text_expr: str, position=None, on_error=None):
    node = {
        "parameters": {
            "method": "POST",
            "url": "=https://api.telegram.org/bot{{ $env.TELEGRAM_BOT_TOKEN }}/sendMessage",
            "sendBody": True,
            "specifyBody": "json",
            "jsonBody": text_expr,
            "options": {
                "timeout": 120000,
            },
        },
        "id": node_id,
        "name": name,
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": position or [0, 0],
    }
    if on_error:
        node["onError"] = on_error
    return node


def sticky(node_id: str, name: str, content: str, position=None, width=360, height=260, color=6):
    return {
        "parameters": {
            "content": content,
            "height": height,
            "width": width,
            "color": color,
        },
        "id": node_id,
        "name": name,
        "type": "n8n-nodes-base.stickyNote",
        "typeVersion": 1,
        "position": position or [0, 0],
    }


IDS = {
    "webhook": "4c828894-a289-4da9-9103-ba6b972446c0",
    "schedule": "04e7dbf6-f597-4a98-8005-4fffea478ca4",
    "normalize_webhook": "acef3e22-e9c9-4184-8f05-a7b4513e611f",
    "validate_webhook": "0418ccf1-b695-4a94-b5df-4ba9ff08fbe2",
    "respond_validation": "dda715bb-61f8-4685-b0dc-0b827892e22f",
    "rss_read": "6cd06824-9746-4ad9-8d39-e7ae7b10a184",
    "normalize_rss": "8ebbfe8a-1c5e-476c-9d40-68f8bab5348d",
    "prepare_runtime": "cb9a1b5d-5846-4a7d-a5eb-a6c333ad224f",
    "check_duplicate": "c6e81aaf-06c6-4852-b699-cbeb4d9f05f3",
    "parse_duplicate": "0e8e29de-86e6-45d0-8d95-f77eb5bd9190",
    "if_duplicate": "249b95bf-077c-48e0-86ab-81a3ec4ad6fc",
    "if_duplicate_webhook": "deebd716-c66b-4056-877c-9ab90884079b",
    "respond_duplicate": "3e78918e-032f-4590-af38-1cee785568dd",
    "download_audio": "5fde06df-b045-40c2-a656-75d6b264b5c5",
    "format_download_error": "01ea2399-d1d8-4f22-ad72-2498ac5a94c6",
    "read_binary": "81ba4bd6-d8f3-4bec-ae68-d6989230862e",
    "whisper_1": "e7082b66-94a7-406c-b977-15e08c2a7cbb",
    "wait_whisper_1": "174365ac-3c4f-4854-bdae-6b1959e5682e",
    "whisper_2": "bd13b588-08b0-4aee-8e0c-bb9595be8dba",
    "wait_whisper_2": "e4028391-62b0-4682-839f-510f1a804c2c",
    "whisper_3": "74f83d09-ac1d-4079-9e6b-30a5a252b70e",
    "wait_whisper_3": "bc2709ee-09e6-45f5-983a-d114944bf6c9",
    "whisper_4": "414a399d-bc8f-4ba3-8ccd-c7b80da3632b",
    "normalize_transcript": "6c692534-0c4d-4976-8852-3e0e15337c41",
    "generate_1": "6e221b0d-e7cb-4b2c-a57e-63a2d6d4728e",
    "wait_generate_1": "e3046b0d-a578-4c7e-a77d-3d9e7e7390a6",
    "generate_2": "5dbadc0e-4668-4496-b103-a38b83cffa49",
    "wait_generate_2": "c2ae2019-c6ea-488b-8c4b-3e6504973935",
    "generate_3": "41159964-99f0-4a71-bf8c-06129055ba4c",
    "wait_generate_3": "b81bde14-0064-4aae-898c-dc80baaa1c6c",
    "generate_4": "52e2a893-89c5-4fce-a3ac-b8ce88d24e73",
    "normalize_post": "80ebca6b-4b3f-445e-aad2-efa097b35f3a",
    "save_draft": "36e30221-daab-4bf1-92d5-3fadd57c3a03",
    "parse_saved": "95c0ad09-d4c5-4b1b-b3cf-46f293494249",
    "telegram_1": "bf82d5db-5c90-44d6-9c97-30da6e6cbacf",
    "wait_telegram": "7a54f9a0-0385-47ce-a1dd-230f43c993e1",
    "telegram_2": "3a7eaa3e-063a-4b98-9188-cc5e9d58b94d",
    "mark_published": "3b3bb756-364c-41ef-94f8-676af609bc87",
    "prepare_success": "4f96dede-88ee-4800-8638-0a33c0441384",
    "if_success_webhook": "fecbb1a7-cd68-42e7-b8ad-4b3087640f1b",
    "respond_success": "ddbc0d42-2a6d-4af2-8c38-df9f08325786",
    "format_transcript_error": "9ebdf4aa-164e-444a-9283-0a9b08eddb2f",
    "format_generation_error": "9ce60111-9944-4d0d-baf5-90907eb06ccc",
    "format_database_error": "d6a98fc5-2b43-492e-b8e6-d131d1ab9012",
    "format_telegram_error": "5a1c7e30-99c2-42c4-8ecc-8f7a3c661b0b",
    "log_error": "f3ff4540-82de-4af1-84e4-7ac33b4b61ae",
    "send_error_alert": "f7ac18df-1629-432b-a2fb-9e822448f8a7",
    "cleanup_error": "24768025-0d52-47c7-b5b4-d492a6920cc3",
    "if_error_webhook": "12524a8e-417e-4535-a029-d8506c0da4af",
    "respond_error": "178d65dc-7774-4fcb-b87a-fca9d7c8e875",
    "finish_background": "a32df7db-ae0b-4c4c-9309-d1226903b241",
    "sticky_overview": "b674ece0-0db5-41ac-b18d-f2dc75fca414",
    "sticky_retry": "896f4447-a514-482a-90cd-bf92c024f2e5",
    "sticky_bonus": "ff292cc5-7fd7-4b4a-ac35-d998b00067eb",
    "format_duplicate_error": "4d3c3efe-c0e7-4d48-8b7c-0928f34afab9",
    "cleanup_success": "b7126659-ccec-4b38-a87b-64841dac5450",
}


format_error_template = """
const source = $('Prepare Runtime Data').item.json;
const rawError = $json.error ?? $json.stderr ?? $json.message ?? 'Unknown error';
const errorMessage = typeof rawError === 'string' ? rawError : JSON.stringify(rawError);
const escapeHtml = (value) => String(value ?? '').replace(/[&<>"]/g, (char) => ({
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
}[char]));
const encode = (value) => Buffer.from(String(value ?? ''), 'utf8').toString('base64');
return {
  json: {
    ...source,
    error_stage: '__STAGE__',
    error_message: errorMessage,
    error_response_code: __CODE__,
    error_message_b64: encode(errorMessage),
    error_input_data_b64: encode(JSON.stringify({
      source_url: source.source_url,
      source_id: source.source_id,
      request_type: source.request_type,
      raw_input: source.raw_input,
    })),
    error_alert_html: `<b>Workflow error</b>\\n<b>Stage:</b> __STAGE__\\n<b>URL:</b> ${escapeHtml(source.source_url)}\\n<b>Message:</b> ${escapeHtml(errorMessage)}`,
  }
};
""".strip()


def format_error_code(stage: str, code: int) -> str:
    return format_error_template.replace("__STAGE__", stage).replace("__CODE__", str(code))


nodes = [
    {
        "parameters": {
            "httpMethod": "POST",
            "path": "news-autoposter",
            "responseMode": "responseNode",
            "options": {},
        },
        "id": IDS["webhook"],
        "name": "Webhook Trigger",
        "type": "n8n-nodes-base.webhook",
        "typeVersion": 2,
        "position": [-1020, 40],
        "webhookId": "20767a28-8f4b-4643-8025-e86d6b3de755",
    },
    {
        "parameters": {
            "rule": {
                "interval": [
                    {
                        "field": "minutes",
                        "minutesInterval": 30,
                    }
                ]
            }
        },
        "id": IDS["schedule"],
        "name": "Schedule Trigger",
        "type": "n8n-nodes-base.scheduleTrigger",
        "typeVersion": 1.2,
        "position": [-1020, 360],
    },
    code_node(
        IDS["normalize_webhook"],
        "Normalize Webhook Input",
        """const body = $json.body ?? {};
const sourceUrl = typeof body.url === 'string' ? body.url.trim() : '';
return {
  json: {
    request_type: 'webhook',
    source_id: body.id ? String(body.id) : $execution.id,
    source_url: sourceUrl,
    raw_input: body,
    validation_error: sourceUrl ? '' : 'Missing required field: url',
  },
};""",
        position=[-780, 40],
    ),
    if_node(
        IDS["validate_webhook"],
        "Validate Webhook Input",
        "={{ $json.validation_error }}",
        {"type": "string", "operation": "isEmpty"},
        position=[-560, 40],
    ),
    respond_node(
        IDS["respond_validation"],
        "Respond Validation Error",
        "={{ ({ status: 'error', message: $json.validation_error }) }}",
        400,
        position=[-320, 220],
    ),
    {
        "parameters": {
            "url": "={{ $env.RSS_FEED_URL }}",
        },
        "id": IDS["rss_read"],
        "name": "RSS Read",
        "type": "n8n-nodes-base.rssFeedRead",
        "typeVersion": 1,
        "position": [-780, 360],
    },
    code_node(
        IDS["normalize_rss"],
        "Normalize RSS Item",
        """const sourceUrl = typeof $json.link === 'string' ? $json.link.trim() : '';
if (!sourceUrl) {
  return [];
}
return {
  json: {
    request_type: 'rss',
    source_id: String($json.guid ?? $json.isoDate ?? $json.link ?? `rss-${$itemIndex}`),
    source_url: sourceUrl,
    raw_input: $json,
    validation_error: '',
  },
};""",
        position=[-560, 360],
    ),
    code_node(
        IDS["prepare_runtime"],
        "Prepare Runtime Data",
        """const sourceId = String($json.source_id || 'item');
const safeId = sourceId
  .toLowerCase()
  .replace(/[^a-z0-9_-]+/g, '-')
  .replace(/^-+|-+$/g, '')
  .slice(0, 40) || 'item';
const tempFilePath = `/tmp/news-autoposter/${$execution.id}-${safeId}.mp3`;
const tempFilePattern = `/tmp/news-autoposter/${$execution.id}-${safeId}.%(ext)s`;
const encode = (value) => Buffer.from(String(value ?? ''), 'utf8').toString('base64');
return {
  json: {
    ...$json,
    temp_file_path: tempFilePath,
    temp_file_pattern: tempFilePattern,
    source_url_b64: encode($json.source_url || ''),
    raw_input_b64: encode(JSON.stringify($json.raw_input ?? {})),
  },
};""",
        position=[-320, 180],
    ),
    execute_command_node(
        IDS["check_duplicate"],
        "Check Duplicate",
        "=python3 /opt/n8n-scripts/db_ops.py check-duplicate --source-url-b64 {{$json.source_url_b64}}",
        position=[-80, 180],
        on_error="continueErrorOutput",
    ),
    code_node(
        IDS["parse_duplicate"],
        "Parse Duplicate Result",
        """const parsed = JSON.parse($json.stdout || '{}');
return {
  json: {
    ...$('Prepare Runtime Data').item.json,
    is_duplicate: Boolean(parsed.exists),
  },
};""",
        position=[160, 180],
    ),
    if_node(
        IDS["if_duplicate"],
        "Is Duplicate?",
        "={{ $json.is_duplicate }}",
        {"type": "boolean", "operation": "true", "singleValue": True},
        position=[380, 180],
    ),
    if_node(
        IDS["if_duplicate_webhook"],
        "Is Webhook Duplicate?",
        "={{ $json.request_type }}",
        {"type": "string", "operation": "equals"},
        right_value="webhook",
        position=[600, 320],
    ),
    respond_node(
        IDS["respond_duplicate"],
        "Respond Duplicate",
        "={{ ({ status: 'duplicate', message: 'This URL has already been processed', source_url: $json.source_url }) }}",
        409,
        position=[840, 240],
    ),
    execute_command_node(
        IDS["download_audio"],
        "Download Audio (yt-dlp)",
        "=/opt/n8n-scripts/download_audio.sh {{ JSON.stringify($json.source_url) }} {{ JSON.stringify($json.temp_file_path) }}",
        position=[620, 40],
        on_error="continueErrorOutput",
    ),
    code_node(
        IDS["format_download_error"],
        "Format Download Error",
        format_error_code("Download Audio", 422),
        position=[860, -120],
    ),
    {
        "parameters": {
            "filePath": "={{ $('Prepare Runtime Data').item.json.temp_file_path }}",
        },
        "id": IDS["read_binary"],
        "name": "Read Binary File",
        "type": "n8n-nodes-base.readBinaryFile",
        "typeVersion": 1,
        "position": [860, 40],
        "onError": "continueErrorOutput",
    },
    {
        "parameters": {
            "method": "POST",
            "url": "https://api.openai.com/v1/audio/transcriptions",
            "sendHeaders": True,
            "headerParameters": {
                "parameters": [
                    {
                        "name": "Authorization",
                        "value": "=Bearer {{ $env.OPENAI_API_KEY }}",
                    }
                ]
            },
            "sendBody": True,
            "contentType": "multipart-form-data",
            "bodyParameters": {
                "parameters": [
                    {"name": "model", "value": "={{ $env.OPENAI_TRANSCRIPTION_MODEL || 'whisper-1' }}"},
                    {
                        "parameterType": "formBinaryData",
                        "name": "file",
                        "inputDataFieldName": "data",
                    },
                    {"name": "language", "value": "ru"},
                ]
            },
            "options": {
                "timeout": 300000,
            },
        },
        "id": IDS["whisper_1"],
        "name": "Transcribe 1",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [1100, 40],
        "onError": "continueErrorOutput",
    },
    wait_node(IDS["wait_whisper_1"], 5, position=[1100, 220], webhook_id="ad5b2e51-8af1-456c-9a99-17ea8059a15b"),
    {
        "parameters": {
            "method": "POST",
            "url": "https://api.openai.com/v1/audio/transcriptions",
            "sendHeaders": True,
            "headerParameters": {
                "parameters": [
                    {
                        "name": "Authorization",
                        "value": "=Bearer {{ $env.OPENAI_API_KEY }}",
                    }
                ]
            },
            "sendBody": True,
            "contentType": "multipart-form-data",
            "bodyParameters": {
                "parameters": [
                    {"name": "model", "value": "={{ $env.OPENAI_TRANSCRIPTION_MODEL || 'whisper-1' }}"},
                    {
                        "parameterType": "formBinaryData",
                        "name": "file",
                        "inputDataFieldName": "data",
                    },
                    {"name": "language", "value": "ru"},
                ]
            },
            "options": {
                "timeout": 300000,
            },
        },
        "id": IDS["whisper_2"],
        "name": "Transcribe 2",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [1340, 220],
        "onError": "continueErrorOutput",
    },
    wait_node(IDS["wait_whisper_2"], 15, position=[1340, 400], webhook_id="29de600a-1310-475f-9f06-25fc54abfc7d"),
    {
        "parameters": {
            "method": "POST",
            "url": "https://api.openai.com/v1/audio/transcriptions",
            "sendHeaders": True,
            "headerParameters": {
                "parameters": [
                    {
                        "name": "Authorization",
                        "value": "=Bearer {{ $env.OPENAI_API_KEY }}",
                    }
                ]
            },
            "sendBody": True,
            "contentType": "multipart-form-data",
            "bodyParameters": {
                "parameters": [
                    {"name": "model", "value": "={{ $env.OPENAI_TRANSCRIPTION_MODEL || 'whisper-1' }}"},
                    {
                        "parameterType": "formBinaryData",
                        "name": "file",
                        "inputDataFieldName": "data",
                    },
                    {"name": "language", "value": "ru"},
                ]
            },
            "options": {
                "timeout": 300000,
            },
        },
        "id": IDS["whisper_3"],
        "name": "Transcribe 3",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [1580, 400],
        "onError": "continueErrorOutput",
    },
    wait_node(IDS["wait_whisper_3"], 30, position=[1580, 580], webhook_id="ab3e2927-7f40-4f32-8577-5192c5119fbb"),
    {
        "parameters": {
            "method": "POST",
            "url": "https://api.openai.com/v1/audio/transcriptions",
            "sendHeaders": True,
            "headerParameters": {
                "parameters": [
                    {
                        "name": "Authorization",
                        "value": "=Bearer {{ $env.OPENAI_API_KEY }}",
                    }
                ]
            },
            "sendBody": True,
            "contentType": "multipart-form-data",
            "bodyParameters": {
                "parameters": [
                    {"name": "model", "value": "={{ $env.OPENAI_TRANSCRIPTION_MODEL || 'whisper-1' }}"},
                    {
                        "parameterType": "formBinaryData",
                        "name": "file",
                        "inputDataFieldName": "data",
                    },
                    {"name": "language", "value": "ru"},
                ]
            },
            "options": {
                "timeout": 300000,
            },
        },
        "id": IDS["whisper_4"],
        "name": "Transcribe 4",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [1820, 580],
        "onError": "continueErrorOutput",
    },
    code_node(
        IDS["normalize_transcript"],
        "Normalize Transcript",
        """const transcript = typeof $json.text === 'string' ? $json.text.trim() : '';
if (!transcript) {
  throw new Error('Whisper response did not include transcript text');
}
const source = $('Prepare Runtime Data').item.json;
const encode = (value) => Buffer.from(String(value ?? ''), 'utf8').toString('base64');
return {
  json: {
    ...source,
    transcript,
    transcript_b64: encode(transcript),
    llm_prompt: [
      'Transform the Russian transcript below into a Telegram news post.',
      'Return JSON only with keys: title, summary, hashtags.',
      'Rules:',
      '- title: concise, factual, max 120 characters',
      '- summary: 2 to 4 short sentences in Russian',
      '- hashtags: array with 3 to 6 hashtags',
      '- do not invent facts',
      '- no markdown, no HTML, no extra keys',
      '',
      `Source URL: ${source.source_url}`,
      '',
      'Transcript:',
      transcript,
    ].join('\\n'),
  },
};""",
        position=[2060, 260],
        on_error="continueErrorOutput",
    ),
    http_json_node(
        IDS["generate_1"],
        "Generate Post 1",
        "https://api.openai.com/v1/chat/completions",
        "={{ JSON.stringify({ model: $env.OPENAI_CHAT_MODEL || 'gpt-4o-mini', temperature: 0.7, response_format: { type: 'json_object' }, messages: [{ role: 'system', content: 'You are a Russian news editor that writes concise Telegram posts and always responds with valid JSON only.' }, { role: 'user', content: $json.llm_prompt }] }) }}",
        position=[2300, 260],
        on_error="continueErrorOutput",
    ),
    wait_node(IDS["wait_generate_1"], 5, position=[2300, 440], webhook_id="11111111-1111-4111-8111-111111111111"),
    http_json_node(
        IDS["generate_2"],
        "Generate Post 2",
        "https://api.openai.com/v1/chat/completions",
        "={{ JSON.stringify({ model: $env.OPENAI_CHAT_MODEL || 'gpt-4o-mini', temperature: 0.7, response_format: { type: 'json_object' }, messages: [{ role: 'system', content: 'You are a Russian news editor that writes concise Telegram posts and always responds with valid JSON only.' }, { role: 'user', content: $json.llm_prompt }] }) }}",
        position=[2540, 440],
        on_error="continueErrorOutput",
    ),
    wait_node(IDS["wait_generate_2"], 15, position=[2540, 620], webhook_id="22222222-2222-4222-8222-222222222222"),
    http_json_node(
        IDS["generate_3"],
        "Generate Post 3",
        "https://api.openai.com/v1/chat/completions",
        "={{ JSON.stringify({ model: $env.OPENAI_CHAT_MODEL || 'gpt-4o-mini', temperature: 0.7, response_format: { type: 'json_object' }, messages: [{ role: 'system', content: 'You are a Russian news editor that writes concise Telegram posts and always responds with valid JSON only.' }, { role: 'user', content: $json.llm_prompt }] }) }}",
        position=[2780, 620],
        on_error="continueErrorOutput",
    ),
    wait_node(IDS["wait_generate_3"], 30, position=[2780, 800], webhook_id="33333333-3333-4333-8333-333333333333"),
    http_json_node(
        IDS["generate_4"],
        "Generate Post 4",
        "https://api.openai.com/v1/chat/completions",
        "={{ JSON.stringify({ model: $env.OPENAI_CHAT_MODEL || 'gpt-4o-mini', temperature: 0.7, response_format: { type: 'json_object' }, messages: [{ role: 'system', content: 'You are a Russian news editor that writes concise Telegram posts and always responds with valid JSON only.' }, { role: 'user', content: $json.llm_prompt }] }) }}",
        position=[3020, 800],
        on_error="continueErrorOutput",
    ),
    code_node(
        IDS["normalize_post"],
        "Normalize Generated Post",
        """const source = $('Normalize Transcript').item.json;
const content = $json.choices?.[0]?.message?.content;
if (!content) {
  throw new Error('OpenAI response missing message content');
}
let parsed;
try {
  parsed = JSON.parse(content);
} catch (error) {
  throw new Error(`OpenAI response was not valid JSON: ${content}`);
}
const title = String(parsed.title || '').trim();
const summary = String(parsed.summary || '').trim();
let hashtags = Array.isArray(parsed.hashtags) ? parsed.hashtags : [];
hashtags = hashtags
  .map((tag) => String(tag).trim())
  .filter(Boolean)
  .map((tag) => (tag.startsWith('#') ? tag : `#${tag.replace(/^#+/, '')}`));
if (!title || !summary || hashtags.length === 0) {
  throw new Error('Generated content missing title, summary, or hashtags');
}
const escapeHtml = (value) => String(value ?? '').replace(/[&<>"]/g, (char) => ({
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
}[char]));
const telegramMessageHtml = `<b>${escapeHtml(title)}</b>\\n\\n${escapeHtml(summary)}\\n\\n${escapeHtml(hashtags.join(' '))}\\n\\n<a href="${source.source_url}">Источник</a>`;
const encode = (value) => Buffer.from(String(value ?? ''), 'utf8').toString('base64');
return {
  json: {
    ...source,
    generated_title: title,
    generated_summary: summary,
    generated_hashtags: hashtags,
    telegram_message_html: telegramMessageHtml,
    post_text_b64: encode(telegramMessageHtml),
  },
};""",
        position=[3260, 520],
        on_error="continueErrorOutput",
    ),
    execute_command_node(
        IDS["save_draft"],
        "Save Draft Post",
        "=python3 /opt/n8n-scripts/db_ops.py insert-post --source-url-b64 {{$json.source_url_b64}} --transcript-b64 {{$json.transcript_b64}} --post-text-b64 {{$json.post_text_b64}} --status draft",
        position=[3500, 520],
        on_error="continueErrorOutput",
    ),
    code_node(
        IDS["parse_saved"],
        "Parse Saved Draft",
        """const parsed = JSON.parse($json.stdout || '{}');
return {
  json: {
    ...$('Normalize Generated Post').item.json,
    post_id: parsed.id,
    post_status: parsed.status,
  },
};""",
        position=[3740, 520],
    ),
    telegram_node(
        IDS["telegram_1"],
        "Send to Telegram 1",
        "={{ JSON.stringify({ chat_id: $env.TELEGRAM_CHAT_ID, text: $json.telegram_message_html, parse_mode: 'HTML', disable_web_page_preview: false }) }}",
        position=[3980, 520],
        on_error="continueErrorOutput",
    ),
    wait_node(IDS["wait_telegram"], 5, position=[3980, 700], webhook_id="44444444-4444-4444-8444-444444444444"),
    telegram_node(
        IDS["telegram_2"],
        "Send to Telegram 2",
        "={{ JSON.stringify({ chat_id: $env.TELEGRAM_CHAT_ID, text: $json.telegram_message_html, parse_mode: 'HTML', disable_web_page_preview: false }) }}",
        position=[4220, 700],
        on_error="continueErrorOutput",
    ),
    execute_command_node(
        IDS["mark_published"],
        "Mark Published",
        "=python3 /opt/n8n-scripts/db_ops.py update-post-status --post-id {{ JSON.stringify($('Parse Saved Draft').item.json.post_id) }} --status published",
        position=[4460, 520],
        on_error="continueErrorOutput",
    ),
    code_node(
        IDS["prepare_success"],
        "Prepare Success Result",
        """const source = $('Prepare Runtime Data').item.json;
const saved = $('Parse Saved Draft').item.json;
return {
  json: {
    ...source,
    post_id: saved.post_id,
    status: 'published',
    telegram_message_html: $('Normalize Generated Post').item.json.telegram_message_html,
  },
};""",
        position=[4700, 520],
    ),
    execute_command_node(
        IDS["cleanup_success"],
        "Cleanup Temp File",
        "=rm -f {{ JSON.stringify($json.temp_file_path) }}",
        position=[4940, 660],
    ),
    if_node(
        IDS["if_success_webhook"],
        "Respond Success?",
        "={{ $json.request_type }}",
        {"type": "string", "operation": "equals"},
        right_value="webhook",
        position=[4940, 520],
    ),
    respond_node(
        IDS["respond_success"],
        "Respond Success",
        "={{ ({ status: 'success', post_id: $json.post_id, source_url: $json.source_url, message: 'Post generated, stored, and sent to Telegram' }) }}",
        201,
        position=[5180, 440],
    ),
    code_node(
        IDS["format_transcript_error"],
        "Format Transcript Error",
        format_error_code("Transcribe (Whisper)", 502),
        position=[2060, 60],
    ),
    code_node(
        IDS["format_generation_error"],
        "Format Generation Error",
        format_error_code("Generate Post", 502),
        position=[3260, 980],
    ),
    code_node(
        IDS["format_database_error"],
        "Format Database Error",
        format_error_code("Database Write", 500),
        position=[4460, 920],
    ),
    code_node(
        IDS["format_telegram_error"],
        "Format Telegram Error",
        format_error_code("Telegram Delivery", 502),
        position=[4460, 760],
    ),
    execute_command_node(
        IDS["log_error"],
        "Log Error",
        "=python3 /opt/n8n-scripts/db_ops.py log-error --node-name {{ JSON.stringify($json.error_stage) }} --error-message-b64 {{$json.error_message_b64}} --input-data-b64 {{$json.error_input_data_b64}}",
        position=[4700, 980],
        on_error="continueErrorOutput",
    ),
    telegram_node(
        IDS["send_error_alert"],
        "Send Error Alert",
        "={{ JSON.stringify({ chat_id: $env.TELEGRAM_CHAT_ID, text: $json.error_alert_html, parse_mode: 'HTML', disable_web_page_preview: true }) }}",
        position=[4700, 840],
        on_error="continueErrorOutput",
    ),
    execute_command_node(
        IDS["cleanup_error"],
        "Cleanup Temp File (Error)",
        "=rm -f {{ JSON.stringify($json.temp_file_path) }}",
        position=[4700, 700],
    ),
    if_node(
        IDS["if_error_webhook"],
        "Respond Error?",
        "={{ $json.request_type }}",
        {"type": "string", "operation": "equals"},
        right_value="webhook",
        position=[4700, 560],
    ),
    respond_node(
        IDS["respond_error"],
        "Respond Error",
        "={{ ({ status: 'error', stage: $json.error_stage, message: $json.error_message, source_url: $json.source_url }) }}",
        "={{ $json.error_response_code }}",
        position=[4940, 500],
    ),
    {
        "parameters": {},
        "id": IDS["finish_background"],
        "name": "Finish Background Path",
        "type": "n8n-nodes-base.noOp",
        "typeVersion": 1,
        "position": [5180, 700],
    },
    sticky(
        IDS["sticky_overview"],
        "Sticky Note Overview",
        "## Main Flow\\n\\nWebhook and Schedule/RSS both normalize into one shared pipeline.\\n\\nThe processing order is: dedupe -> download -> transcription -> AI post generation -> draft save -> Telegram -> publish status update.\\n\\nThe workflow is intentionally portable: OpenAI and Telegram use env vars, while DB operations and yt-dlp are handled through mounted helper scripts inside the n8n container.",
        position=[-1240, -340],
        width=420,
        height=320,
        color=6,
    ),
    sticky(
        IDS["sticky_retry"],
        "Sticky Note Retry",
        "## Retries and Reliability\\n\\nWhisper and OpenAI generation use explicit retry branches with waits of 5s, 15s, and 30s.\\n\\nTelegram delivery retries once after 5s.\\n\\nEvery failure is normalized, logged to `error_logs`, sent to Telegram as an alert, and triggers temp-file cleanup in `/tmp/news-autoposter`.",
        position=[1880, -340],
        width=420,
        height=300,
        color=5,
    ),
    sticky(
        IDS["sticky_bonus"],
        "Sticky Note Bonus",
        "## Bonus Tasks\\n\\nDeduplication happens before any expensive work and returns `409` for webhook requests.\\n\\nThe `Schedule Trigger` + `RSS Read` path polls the configured RSS feed and reuses the same processing pipeline as the webhook path.\\n\\nBackground RSS executions do not emit webhook responses, they simply finish after success, duplicate skip, or error handling.",
        position=[-1240, 520],
        width=420,
        height=300,
        color=4,
    ),
    code_node(
        IDS["format_duplicate_error"],
        "Format Duplicate Check Error",
        format_error_code("Duplicate Check", 500),
        position=[160, -40],
    ),
]


connections = {
    "Webhook Trigger": {"main": [[connection("Normalize Webhook Input")]]},
    "Normalize Webhook Input": {"main": [[connection("Validate Webhook Input")]]},
    "Validate Webhook Input": {
        "main": [
            [connection("Prepare Runtime Data")],
            [connection("Respond Validation Error")],
        ]
    },
    "Schedule Trigger": {"main": [[connection("RSS Read")]]},
    "RSS Read": {"main": [[connection("Normalize RSS Item")]]},
    "Normalize RSS Item": {"main": [[connection("Prepare Runtime Data")]]},
    "Prepare Runtime Data": {"main": [[connection("Check Duplicate")]]},
    "Check Duplicate": {
        "main": [
            [connection("Parse Duplicate Result")],
            [connection("Format Duplicate Check Error")],
        ]
    },
    "Parse Duplicate Result": {"main": [[connection("Is Duplicate?")]]},
    "Is Duplicate?": {
        "main": [
            [connection("Download Audio (yt-dlp)")],
            [connection("Is Webhook Duplicate?")],
        ]
    },
    "Is Webhook Duplicate?": {
        "main": [
            [connection("Respond Duplicate")],
            [connection("Finish Background Path")],
        ]
    },
    "Download Audio (yt-dlp)": {
        "main": [
            [connection("Read Binary File")],
            [connection("Format Download Error")],
        ]
    },
    "Read Binary File": {
        "main": [
            [connection("Transcribe 1")],
            [connection("Format Download Error")],
        ]
    },
    "Transcribe 1": {
        "main": [
            [connection("Normalize Transcript")],
            [connection("Wait 5s", 0)],
        ]
    },
    "Wait 5s": {"main": [[connection("Transcribe 2")]]},
    "Transcribe 2": {
        "main": [
            [connection("Normalize Transcript")],
            [connection("Wait 15s", 0)],
        ]
    },
    "Wait 15s": {"main": [[connection("Transcribe 3")]]},
    "Transcribe 3": {
        "main": [
            [connection("Normalize Transcript")],
            [connection("Wait 30s", 0)],
        ]
    },
    "Wait 30s": {"main": [[connection("Transcribe 4")]]},
    "Transcribe 4": {
        "main": [
            [connection("Normalize Transcript")],
            [connection("Format Transcript Error")],
        ]
    },
    "Normalize Transcript": {
        "main": [
            [connection("Generate Post 1")],
            [connection("Format Transcript Error")],
        ]
    },
    "Generate Post 1": {
        "main": [
            [connection("Normalize Generated Post")],
            [connection("Wait 5s", 0)],
        ]
    },
    "Generate Post 2": {
        "main": [
            [connection("Normalize Generated Post")],
            [connection("Wait 15s", 0)],
        ]
    },
    "Generate Post 3": {
        "main": [
            [connection("Normalize Generated Post")],
            [connection("Wait 30s", 0)],
        ]
    },
    "Generate Post 4": {
        "main": [
            [connection("Normalize Generated Post")],
            [connection("Format Generation Error")],
        ]
    },
    "Normalize Generated Post": {
        "main": [
            [connection("Save Draft Post")],
            [connection("Format Generation Error")],
        ]
    },
    "Save Draft Post": {
        "main": [
            [connection("Parse Saved Draft")],
            [connection("Format Database Error")],
        ]
    },
    "Parse Saved Draft": {"main": [[connection("Send to Telegram 1")]]},
    "Send to Telegram 1": {
        "main": [
            [connection("Mark Published")],
            [connection("Wait 5s", 0)],
        ]
    },
    "Send to Telegram 2": {
        "main": [
            [connection("Mark Published")],
            [connection("Format Telegram Error")],
        ]
    },
    "Mark Published": {
        "main": [
            [connection("Prepare Success Result")],
            [connection("Format Database Error")],
        ]
    },
    "Prepare Success Result": {
        "main": [
            [connection("Respond Success?")],
            [connection("Cleanup Temp File")],
        ]
    },
    "Respond Success?": {
        "main": [
            [connection("Respond Success")],
            [connection("Finish Background Path")],
        ]
    },
    "Format Duplicate Check Error": {
        "main": [
            [connection("Log Error"), connection("Send Error Alert"), connection("Cleanup Temp File (Error)"), connection("Respond Error?")],
        ]
    },
    "Format Download Error": {
        "main": [
            [connection("Log Error"), connection("Send Error Alert"), connection("Cleanup Temp File (Error)"), connection("Respond Error?")],
        ]
    },
    "Format Transcript Error": {
        "main": [
            [connection("Log Error"), connection("Send Error Alert"), connection("Cleanup Temp File (Error)"), connection("Respond Error?")],
        ]
    },
    "Format Generation Error": {
        "main": [
            [connection("Log Error"), connection("Send Error Alert"), connection("Cleanup Temp File (Error)"), connection("Respond Error?")],
        ]
    },
    "Format Database Error": {
        "main": [
            [connection("Log Error"), connection("Send Error Alert"), connection("Cleanup Temp File (Error)"), connection("Respond Error?")],
        ]
    },
    "Format Telegram Error": {
        "main": [
            [connection("Log Error"), connection("Send Error Alert"), connection("Cleanup Temp File (Error)"), connection("Respond Error?")],
        ]
    },
    "Respond Error?": {
        "main": [
            [connection("Respond Error")],
            [connection("Finish Background Path")],
        ]
    },
    "Wait 5s": {"main": [[connection("Generate Post 2")]]},
    "Wait 15s": {"main": [[connection("Generate Post 3")]]},
    "Wait 30s": {"main": [[connection("Generate Post 4")]]},
}


# Fix connection key collisions for identically named wait nodes
connections["Transcribe 1"] = {
    "main": [
        [connection("Normalize Transcript")],
        [connection("Wait 5s", 0)],
    ]
}
connections["Wait 5s"] = {"main": [[connection("Transcribe 2")]]}
connections["Transcribe 2"] = {
    "main": [
        [connection("Normalize Transcript")],
        [connection("Wait 15s", 0)],
    ]
}
connections["Wait 15s"] = {"main": [[connection("Transcribe 3")]]}
connections["Transcribe 3"] = {
    "main": [
        [connection("Normalize Transcript")],
        [connection("Wait 30s", 0)],
    ]
}
connections["Wait 30s"] = {"main": [[connection("Transcribe 4")]]}

# Reassign uniquely named wait nodes used after generation and Telegram
for node in nodes:
    if node["id"] == IDS["wait_generate_1"]:
        node["name"] = "Wait 5s (Generate)"
    if node["id"] == IDS["wait_generate_2"]:
        node["name"] = "Wait 15s (Generate)"
    if node["id"] == IDS["wait_generate_3"]:
        node["name"] = "Wait 30s (Generate)"
    if node["id"] == IDS["wait_telegram"]:
        node["name"] = "Wait 5s (Telegram)"
    if node["id"] == IDS["wait_whisper_1"]:
        node["name"] = "Wait 5s (Whisper)"
    if node["id"] == IDS["wait_whisper_2"]:
        node["name"] = "Wait 15s (Whisper)"
    if node["id"] == IDS["wait_whisper_3"]:
        node["name"] = "Wait 30s (Whisper)"

connections["Transcribe 1"] = {
    "main": [
        [connection("Normalize Transcript")],
        [connection("Wait 5s (Whisper)")],
    ]
}
connections["Wait 5s (Whisper)"] = {"main": [[connection("Transcribe 2")]]}
connections["Transcribe 2"] = {
    "main": [
        [connection("Normalize Transcript")],
        [connection("Wait 15s (Whisper)")],
    ]
}
connections["Wait 15s (Whisper)"] = {"main": [[connection("Transcribe 3")]]}
connections["Transcribe 3"] = {
    "main": [
        [connection("Normalize Transcript")],
        [connection("Wait 30s (Whisper)")],
    ]
}
connections["Wait 30s (Whisper)"] = {"main": [[connection("Transcribe 4")]]}

connections["Generate Post 1"] = {
    "main": [
        [connection("Normalize Generated Post")],
        [connection("Wait 5s (Generate)")],
    ]
}
connections["Wait 5s (Generate)"] = {"main": [[connection("Generate Post 2")]]}
connections["Generate Post 2"] = {
    "main": [
        [connection("Normalize Generated Post")],
        [connection("Wait 15s (Generate)")],
    ]
}
connections["Wait 15s (Generate)"] = {"main": [[connection("Generate Post 3")]]}
connections["Generate Post 3"] = {
    "main": [
        [connection("Normalize Generated Post")],
        [connection("Wait 30s (Generate)")],
    ]
}
connections["Wait 30s (Generate)"] = {"main": [[connection("Generate Post 4")]]}

connections["Send to Telegram 1"] = {
    "main": [
        [connection("Mark Published")],
        [connection("Wait 5s (Telegram)")],
    ]
}
connections["Wait 5s (Telegram)"] = {"main": [[connection("Send to Telegram 2")]]}

for obsolete_name in ("Wait 5s", "Wait 15s", "Wait 30s"):
    connections.pop(obsolete_name, None)


workflow = {
    "name": "Goodini News Autoposter",
    "nodes": nodes,
    "pinData": {},
    "connections": connections,
    "active": False,
    "settings": {
        "executionOrder": "v1",
    },
    "versionId": "9da2d2be-0dea-45d5-bfb7-18ea0c79c833",
    "meta": {
        "templateCredsSetupCompleted": True,
    },
    "id": "goodiniNewsAutoposter",
    "tags": [
        {
            "name": "тестовое-задание",
            "id": "n0Y74dIZYwwvIEcr",
        }
    ],
}


WORKFLOW_PATH.write_text(json.dumps(workflow, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
