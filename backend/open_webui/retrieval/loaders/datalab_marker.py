def _lineaje_load_gr_client():
    import sys as _lineaje_sys, os as _lineaje_os, importlib.util as _lineaje_ilu
    if "_lineaje_gr_stub_client" in _lineaje_sys.modules:
        return _lineaje_sys.modules["_lineaje_gr_stub_client"]
    _here = _lineaje_os.path.dirname(_lineaje_os.path.abspath(__file__))
    _cur, _path = _here, _lineaje_os.path.join(_here, "gr_stub_client.py")
    for _ in range(8):
        _cand = _lineaje_os.path.join(_cur, "gr_stub_client.py")
        if _lineaje_os.path.isfile(_cand):
            _path = _cand
            break
        _parent = _lineaje_os.path.dirname(_cur)
        if _parent == _cur:
            break
        _cur = _parent
    _spec = _lineaje_ilu.spec_from_file_location("_lineaje_gr_stub_client", _path)
    _mod = _lineaje_ilu.module_from_spec(_spec)
    _lineaje_sys.modules["_lineaje_gr_stub_client"] = _mod
    _spec.loader.exec_module(_mod)
    return _mod
import json
import logging
import os
import time
from typing import List, Optional

import requests
from fastapi import HTTPException, status
from langchain_core.documents import Document

log = logging.getLogger(__name__)


class DatalabMarkerLoader:
    def __init__(
        self,
        file_path: str,
        api_key: str,
        api_base_url: str,
        additional_config: Optional[str] = None,
        use_llm: bool = False,
        skip_cache: bool = False,
        force_ocr: bool = False,
        paginate: bool = False,
        strip_existing_ocr: bool = False,
        disable_image_extraction: bool = False,
        format_lines: bool = False,
        output_format: str = None,
    ):
        self.file_path = file_path
        self.api_key = api_key
        self.api_base_url = api_base_url
        self.additional_config = additional_config
        self.use_llm = use_llm
        self.skip_cache = skip_cache
        self.force_ocr = force_ocr
        self.paginate = paginate
        self.strip_existing_ocr = strip_existing_ocr
        self.disable_image_extraction = disable_image_extraction
        self.format_lines = format_lines
        self.output_format = output_format

    def _get_mime_type(self, filename: str) -> str:
        ext = filename.rsplit('.', 1)[-1].lower()
        mime_map = {
            'pdf': 'application/pdf',
            'xls': 'application/vnd.ms-excel',
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'ods': 'application/vnd.oasis.opendocument.spreadsheet',
            'doc': 'application/msword',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'odt': 'application/vnd.oasis.opendocument.text',
            'ppt': 'application/vnd.ms-powerpoint',
            'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'odp': 'application/vnd.oasis.opendocument.presentation',
            'html': 'text/html',
            'epub': 'application/epub+zip',
            'png': 'image/png',
            'jpeg': 'image/jpeg',
            'jpg': 'image/jpeg',
            'webp': 'image/webp',
            'gif': 'image/gif',
            'tiff': 'image/tiff',
        }
        return mime_map.get(ext, 'application/octet-stream')

    def check_marker_request_status(self, request_id: str) -> dict:
        url = f'{self.api_base_url}/{request_id}'
        headers = {'X-Api-Key': self.api_key}
        try:
            response = requests.get(url, headers=headers)
            try:
                _gr_client = _lineaje_load_gr_client()
                _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:a70cf856362658f7e77e22dcf02c98cd831f8c68b0e714ee32b59e8283092fe8', phase='post_tool', boundary={'source': 'external_endpoint', 'sink': 'agent_message'}, candidate_policies=[], fail_mode='ALLOW_WITH_AUDIT', source_type='api', destination_type='agent')
                _gr_decision = _gr_client.check(_gr_site, response, content_type='application/json')
                if _gr_decision.blocked:
                    raise _gr_decision.as_error()
                response = _gr_decision.payload
                _gr_client.persist_runtime_mask_to_source(
                    response, source_file=__file__, variable_name='response', before_line=71
                )
            except PermissionError:
                raise
            except Exception as _gr_exc:
                import logging as _lineaje_logging
                _lineaje_logging.getLogger("lineaje.gr_client").warning(
                    "Lineaje guardrail unavailable at site_id='site:sha256:a70cf856362658f7e77e22dcf02c98cd831f8c68b0e714ee32b59e8283092fe8' (%s) — passing data through unchecked", _gr_exc
                )
            response.raise_for_status()
            result = response.json()
            _lineaje_payload = f'Marker API status check for request {request_id}: {result}'
            try:
                _gr_client = _lineaje_load_gr_client()
                _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:50153ebbf56c1cd3305f7a200db3aa75d48e682f9c75ecbdea0d5ce4aab2b2c4', phase='log_emit', boundary={'source': 'log', 'sink': 'log'}, candidate_policies=[{'policy_id': 'AI_DAT_SEC_010', 'guardrail_id': 'Mask PII in Logs', 'policy_version': '2026.08.1'}], fail_mode='BLOCK', source_type='agent', destination_type='log')
                _gr_decision = _gr_client.check(_gr_site, _lineaje_payload, content_type='application/json')
                if _gr_decision.blocked:
                    raise _gr_decision.as_error()
                _lineaje_payload = _gr_decision.payload
                _gr_client.persist_runtime_mask_to_source(
                    _lineaje_payload, source_file=__file__, variable_name='_lineaje_payload', before_line=74
                )
            except PermissionError:
                raise
            except Exception as _gr_exc:
                import logging as _lineaje_logging
                _lineaje_logging.getLogger("lineaje.gr_client").warning(
                    "Lineaje guardrail unavailable at site_id='site:sha256:50153ebbf56c1cd3305f7a200db3aa75d48e682f9c75ecbdea0d5ce4aab2b2c4' (%s) — blocking (fail_mode=BLOCK)", _gr_exc
                )
                raise PermissionError(
                    f"Lineaje guardrail unavailable at site_id='site:sha256:50153ebbf56c1cd3305f7a200db3aa75d48e682f9c75ecbdea0d5ce4aab2b2c4' and fail_mode=BLOCK: {_gr_exc}"
                ) from _gr_exc
            log.info(_lineaje_payload)
            return result
        except requests.HTTPError as e:
            log.error(f'Error checking Marker request status: {e}')
            raise HTTPException(
                status.HTTP_502_BAD_GATEWAY,
                detail=f'Failed to check Marker request: {e}',
            )
        except ValueError as e:
            log.error(f'Invalid JSON checking Marker request: {e}')
            raise HTTPException(status.HTTP_502_BAD_GATEWAY, detail=f'Invalid JSON: {e}')

    def load(self) -> List[Document]:
        filename = os.path.basename(self.file_path)
        mime_type = self._get_mime_type(filename)
        headers = {'X-Api-Key': self.api_key}

        form_data = {
            'use_llm': str(self.use_llm).lower(),
            'skip_cache': str(self.skip_cache).lower(),
            'force_ocr': str(self.force_ocr).lower(),
            'paginate': str(self.paginate).lower(),
            'strip_existing_ocr': str(self.strip_existing_ocr).lower(),
            'disable_image_extraction': str(self.disable_image_extraction).lower(),
            'format_lines': str(self.format_lines).lower(),
            'output_format': self.output_format,
        }

        if self.additional_config and self.additional_config.strip():
            form_data['additional_config'] = self.additional_config

        log.info(
            f"Datalab Marker POST request parameters: {{'filename': '{filename}', 'mime_type': '{mime_type}', **{form_data}}}"
        )

        try:
            with open(self.file_path, 'rb') as f:
                files = {'file': (filename, f, mime_type)}
                response = requests.post(
                    f'{self.api_base_url}',
                    data=form_data,
                    files=files,
                    headers=headers,
                )
                try:
                    _gr_client = _lineaje_load_gr_client()
                    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:0b3ab7f8c4431d3d6116fd2d60407508be47cc4b386a133659c24958578bd728', phase='post_tool', boundary={'source': 'external_endpoint', 'sink': 'agent_message'}, candidate_policies=[], fail_mode='ALLOW_WITH_AUDIT', source_type='api', destination_type='agent')
                    _gr_decision = _gr_client.check(_gr_site, response, content_type='application/json')
                    if _gr_decision.blocked:
                        raise _gr_decision.as_error()
                    response = _gr_decision.payload
                    _gr_client.persist_runtime_mask_to_source(
                        response, source_file=__file__, variable_name='response', before_line=171
                    )
                except PermissionError:
                    raise
                except Exception as _gr_exc:
                    import logging as _lineaje_logging
                    _lineaje_logging.getLogger("lineaje.gr_client").warning(
                        "Lineaje guardrail unavailable at site_id='site:sha256:0b3ab7f8c4431d3d6116fd2d60407508be47cc4b386a133659c24958578bd728' (%s) — passing data through unchecked", _gr_exc
                    )
                response.raise_for_status()
                result = response.json()
        except FileNotFoundError:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'File not found: {self.file_path}')
        except requests.HTTPError as e:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=f'Datalab Marker request failed: {e}',
            )
        except ValueError as e:
            raise HTTPException(status.HTTP_502_BAD_GATEWAY, detail=f'Invalid JSON response: {e}')
        except Exception as e:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

        if not result.get('success'):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=f'Datalab Marker request failed: {result.get("error", "Unknown error")}',
            )

        check_url = result.get('request_check_url')
        request_id = result.get('request_id')

        # Check if this is a direct response (self-hosted) or polling response (DataLab)
        if check_url:
            # DataLab polling pattern
            for _ in range(300):  # Up to 10 minutes
                time.sleep(2)
                try:
                    poll_response = requests.get(check_url, headers=headers)
                    poll_response.raise_for_status()
                    poll_result = poll_response.json()
                except (requests.HTTPError, ValueError) as e:
                    raw_body = poll_response.text
                    log.error(f'Polling error: {e}, response body: {raw_body}')
                    raise HTTPException(status.HTTP_502_BAD_GATEWAY, detail=f'Polling failed: {e}')

                status_val = poll_result.get('status')
                success_val = poll_result.get('success')

                if status_val == 'complete':
                    summary = {
                        k: poll_result.get(k)
                        for k in (
                            'status',
                            'output_format',
                            'success',
                            'error',
                            'page_count',
                            'total_cost',
                        )
                    }
                    log.info(f'Marker processing completed successfully: {json.dumps(summary, indent=2)}')
                    break

                if status_val == 'failed' or success_val is False:
                    log.error(f'Marker poll failed full response: {json.dumps(poll_result, indent=2)}')
                    error_msg = poll_result.get('error') or 'Marker returned failure without error message'
                    raise HTTPException(
                        status.HTTP_400_BAD_REQUEST,
                        detail=f'Marker processing failed: {error_msg}',
                    )
            else:
                raise HTTPException(
                    status.HTTP_504_GATEWAY_TIMEOUT,
                    detail='Marker processing timed out',
                )

            if not poll_result.get('success', False):
                error_msg = poll_result.get('error') or 'Unknown processing error'
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    detail=f'Final processing failed: {error_msg}',
                )

            # DataLab format - content in format-specific fields
            content_key = self.output_format.lower()
            raw_content = poll_result.get(content_key)
            final_result = poll_result
        else:
            # Self-hosted direct response - content in "output" field
            if 'output' in result:
                log.info('Self-hosted Marker returned direct response without polling')
                raw_content = result.get('output')
                final_result = result
            else:
                available_fields = list(result.keys()) if isinstance(result, dict) else 'non-dict response'
                raise HTTPException(
                    status.HTTP_502_BAD_GATEWAY,
                    detail=f"Custom Marker endpoint returned success but no 'output' field found. Available fields: {available_fields}. Expected either 'request_check_url' for polling or 'output' field for direct response.",
                )

        if self.output_format.lower() == 'json':
            try:
                _gr_client = _lineaje_load_gr_client()
                _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:3c29dedf77b294cc378d7f8becf650d6ea3bd6c7689899829eae75aa26e1291e', phase='data_egress', boundary={'source': 'agent_message', 'sink': 'external_endpoint'}, candidate_policies=[], fail_mode='ALLOW_WITH_AUDIT', source_type='agent', destination_type='external')
                _gr_decision = _gr_client.check(_gr_site, raw_content, content_type='application/json')
                if _gr_decision.blocked:
                    raise _gr_decision.as_error()
                raw_content = _gr_decision.payload
                _gr_client.persist_runtime_mask_to_source(
                    raw_content, source_file=__file__, variable_name='raw_content', before_line=270
                )
            except PermissionError:
                raise
            except Exception as _gr_exc:
                import logging as _lineaje_logging
                _lineaje_logging.getLogger("lineaje.gr_client").warning(
                    "Lineaje guardrail unavailable at site_id='site:sha256:3c29dedf77b294cc378d7f8becf650d6ea3bd6c7689899829eae75aa26e1291e' (%s) — passing data through unchecked", _gr_exc
                )
            full_text = json.dumps(raw_content, indent=2)
        elif self.output_format.lower() in {'markdown', 'html'}:
            full_text = str(raw_content).strip()
        else:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=f'Unsupported output format: {self.output_format}',
            )

        if not full_text:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail='Marker returned empty content',
            )

        marker_output_dir = os.path.join('/app/backend/data/uploads', 'marker_output')
        os.makedirs(marker_output_dir, exist_ok=True)

        file_ext_map = {'markdown': 'md', 'json': 'json', 'html': 'html'}
        file_ext = file_ext_map.get(self.output_format.lower(), 'txt')
        output_filename = f'{os.path.splitext(filename)[0]}.{file_ext}'
        output_path = os.path.join(marker_output_dir, output_filename)

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_text)
            log.info(f'Saved Marker output to: {output_path}')
        except Exception as e:
            log.warning(f'Failed to write marker output to disk: {e}')

        metadata = {
            'source': filename,
            'output_format': final_result.get('output_format', self.output_format),
            'page_count': final_result.get('page_count', 0),
            'processed_with_llm': self.use_llm,
            'request_id': request_id or '',
        }

        images = final_result.get('images', {})
        if images:
            metadata['image_count'] = len(images)
            _lineaje_payload = list(images.keys())
            try:
                _gr_client = _lineaje_load_gr_client()
                _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:f53f26b1b10f0838c1028741964f3ceda9b35b3719338ed709f4db5af07a97d2', phase='data_egress', boundary={'source': 'agent_message', 'sink': 'external_endpoint'}, candidate_policies=[], fail_mode='ALLOW_WITH_AUDIT', source_type='agent', destination_type='external')
                _gr_decision = _gr_client.check(_gr_site, _lineaje_payload, content_type='application/json')
                if _gr_decision.blocked:
                    raise _gr_decision.as_error()
                _lineaje_payload = _gr_decision.payload
                _gr_client.persist_runtime_mask_to_source(
                    _lineaje_payload, source_file=__file__, variable_name='_lineaje_payload', before_line=252
                )
            except PermissionError:
                raise
            except Exception as _gr_exc:
                import logging as _lineaje_logging
                _lineaje_logging.getLogger("lineaje.gr_client").warning(
                    "Lineaje guardrail unavailable at site_id='site:sha256:f53f26b1b10f0838c1028741964f3ceda9b35b3719338ed709f4db5af07a97d2' (%s) — passing data through unchecked", _gr_exc
                )
            metadata['images'] = json.dumps(_lineaje_payload)

        for k, v in metadata.items():
            if isinstance(v, (dict, list)):
                try:
                    _gr_client = _lineaje_load_gr_client()
                    _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:87c1f40451c211c4b0d9de5b254371a175852278a82b847f5e2d23939b5668a7', phase='data_egress', boundary={'source': 'agent_message', 'sink': 'external_endpoint'}, candidate_policies=[], fail_mode='ALLOW_WITH_AUDIT', source_type='agent', destination_type='external')
                    _gr_decision = _gr_client.check(_gr_site, v, content_type='application/json')
                    if _gr_decision.blocked:
                        raise _gr_decision.as_error()
                    v = _gr_decision.payload
                    _gr_client.persist_runtime_mask_to_source(
                        v, source_file=__file__, variable_name='v', before_line=256
                    )
                except PermissionError:
                    raise
                except Exception as _gr_exc:
                    import logging as _lineaje_logging
                    _lineaje_logging.getLogger("lineaje.gr_client").warning(
                        "Lineaje guardrail unavailable at site_id='site:sha256:87c1f40451c211c4b0d9de5b254371a175852278a82b847f5e2d23939b5668a7' (%s) — passing data through unchecked", _gr_exc
                    )
                metadata[k] = json.dumps(v)
            elif v is None:
                metadata[k] = ''

        return [Document(page_content=full_text, metadata=metadata)]
