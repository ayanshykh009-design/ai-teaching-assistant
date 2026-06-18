import json
import os
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid


def check(name, expected, actual, good_ref, fail_ref):
    if actual in expected:
        print(f"  PASS [{actual}] {name}")
        good_ref[0] += 1
    else:
        print(f"  FAIL [{actual}] {name} (expected {expected})")
        fail_ref[0] += 1


def multipart_request(url, field_name, filename, data, method="POST"):
    boundary = "----" + uuid.uuid4().hex
    body_parts = [
        f"--{boundary}".encode(),
        f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"'.encode(),
        b"Content-Type: application/javascript",
        b"",
        data if isinstance(data, bytes) else data.encode(),
        f"--{boundary}--".encode(),
    ]
    body_bytes = b"\r\n".join(body_parts)
    req = urllib.request.Request(url, method=method)
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    req.add_header("Content-Length", str(len(body_bytes)))
    return req, body_bytes


def kill_port(port):
    """Kill any process listening on the given port."""
    import subprocess as sp
    try:
        out = sp.check_output(f"netstat -ano | findstr :{port}", shell=True, text=True)
        for line in out.strip().splitlines():
            parts = line.split()
            if len(parts) >= 5:
                pid = parts[-1]
                try:
                    os.kill(int(pid), signal.SIGTERM)
                except (OSError, ValueError):
                    pass
    except Exception:
        pass
    time.sleep(1)


def main():
    kill_port(8000)
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd="D:/ai-teaching-assistant",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(15)

    good = [0]
    fail = [0]
    sample_code = b"function test() { return 1; }"

    try:
        # === PHASE 1 ===
        print("=== PHASE 1 ===")
        r = urllib.request.urlopen("http://127.0.0.1:8000/", timeout=5)
        check("GET /", {"200"}, str(r.status), good, fail)

        req, body = multipart_request("http://127.0.0.1:8000/upload", "file", "test.js", sample_code)
        try:
            r = urllib.request.urlopen(req, data=body, timeout=30)
            check("POST /upload (valid)", {"200", "502"}, str(r.status), good, fail)
        except urllib.error.HTTPError as e:
            check("POST /upload (valid)", {"200", "502"}, str(e.code), good, fail)

        req2 = urllib.request.Request("http://127.0.0.1:8000/upload", method="POST")
        try:
            urllib.request.urlopen(req2, timeout=5)
        except urllib.error.HTTPError as e:
            check("POST /upload (no file)", {"422"}, str(e.code), good, fail)

        # === PHASE 2 ===
        print("\n=== PHASE 2 ===")
        req3, body3 = multipart_request("http://127.0.0.1:8000/review", "file", "test.js", sample_code)
        try:
            r3 = urllib.request.urlopen(req3, data=body3, timeout=180)
            check("POST /review (valid)", {"200"}, str(r3.status), good, fail)
            j3 = json.loads(r3.read())
            for k in ["code_review", "tutor_explanation", "rubric", "feedback"]:
                check(f"  {k} present", {"True"}, str(k in j3), good, fail)
        except urllib.error.HTTPError as e:
            check("POST /review (valid)", {"200"}, str(e.code), good, fail)

        req4 = urllib.request.Request("http://127.0.0.1:8000/review", method="POST")
        try:
            urllib.request.urlopen(req4, timeout=5)
        except urllib.error.HTTPError as e:
            check("POST /review (no file)", {"422"}, str(e.code), good, fail)

        # === PHASE 3 ===
        print("\n=== PHASE 3 ===")
        req5 = urllib.request.Request("http://127.0.0.1:8000/knowledge/ingest", method="POST")
        try:
            r5 = urllib.request.urlopen(req5, timeout=120)
            check("POST /knowledge/ingest", {"200"}, str(r5.status), good, fail)
            j5 = json.loads(r5.read())
            check(f"  total_points >= 8", {"True"}, str(j5.get("total_points", 0) >= 8), good, fail)
        except urllib.error.HTTPError as e:
            check("POST /knowledge/ingest", {"200"}, str(e.code), good, fail)

        try:
            r6 = urllib.request.urlopen("http://127.0.0.1:8000/knowledge/stats", timeout=10)
            check("GET /knowledge/stats", {"200"}, str(r6.status), good, fail)
            j6 = json.loads(r6.read())
            check(f"  5 collections", {"True"}, str(len(j6.get("collections", {})) == 5), good, fail)
        except urllib.error.HTTPError as e:
            check("GET /knowledge/stats", {"200"}, str(e.code), good, fail)

        try:
            r7 = urllib.request.urlopen(
                "http://127.0.0.1:8000/knowledge/search?q=javascript+function&collection=notes&limit=3", timeout=10
            )
            check("GET /knowledge/search", {"200"}, str(r7.status), good, fail)
        except urllib.error.HTTPError as e:
            check("GET /knowledge/search", {"200"}, str(e.code), good, fail)

        try:
            urllib.request.urlopen("http://127.0.0.1:8000/knowledge/search?q=&collection=notes", timeout=5)
        except urllib.error.HTTPError as e:
            check("GET /knowledge/search?q= (empty)", {"400"}, str(e.code), good, fail)

        add_data = json.dumps({"collection": "notes", "text": "test doc", "source": "test"}).encode()
        req8 = urllib.request.Request(
            "http://127.0.0.1:8000/knowledge/add",
            method="POST",
            data=add_data,
            headers={"Content-Type": "application/json"},
        )
        try:
            r8 = urllib.request.urlopen(req8, timeout=30)
            check("POST /knowledge/add", {"200"}, str(r8.status), good, fail)
        except urllib.error.HTTPError as e:
            check("POST /knowledge/add", {"200", "422"}, str(e.code), good, fail)

        # Auth test (auth disabled by default — verify health is accessible)
        try:
            ra = urllib.request.urlopen("http://127.0.0.1:8000/", timeout=5)
            ja = json.loads(ra.read())
            check("Auth disabled (health accessible)", {"True"}, str(ja.get("auth_enabled") is False), good, fail)
        except Exception as e:
            print(f"\n  AUTH TEST ERROR: {e}")
            fail[0] += 1

        # File check fields present in review response
        try:
            req_fc, body_fc = multipart_request("http://127.0.0.1:8000/review", "file", "app.js", sample_code)
            r_fc = urllib.request.urlopen(req_fc, data=body_fc, timeout=180)
            j_fc = json.loads(r_fc.read())
            cr = j_fc.get("code_review", {})
            has_fc = "filename_check" in cr
            has_sc = "structure_check" in cr
            has_cc = "corrected_code" in cr
            check("filename_check in review", {"True"}, str(has_fc), good, fail)
            check("structure_check in review", {"True"}, str(has_sc), good, fail)
            check("corrected_code in review", {"True"}, str(has_cc), good, fail)
        except urllib.error.HTTPError as e:
            check("filename_check in review (HTTP)", {"200"}, str(e.code), good, fail)

        # Edge cases
        try:
            add_empty = json.dumps({"collection": "notes", "text": "", "source": "test"}).encode()
            req_empty = urllib.request.Request(
                "http://127.0.0.1:8000/knowledge/add", method="POST", data=add_empty,
                headers={"Content-Type": "application/json"},
            )
            urllib.request.urlopen(req_empty, timeout=5)
        except urllib.error.HTTPError as e:
            check("POST /knowledge/add (empty text)", {"400"}, str(e.code), good, fail)

        try:
            urllib.request.urlopen(
                "http://127.0.0.1:8000/knowledge/search?q=test&collection=invalid", timeout=5
            )
        except urllib.error.HTTPError as e:
            check("GET /knowledge/search (bad collection)", {"500"}, str(e.code), good, fail)

        try:
            req_del = urllib.request.Request(
                "http://127.0.0.1:8000/knowledge/notes/nonexistent-id", method="DELETE"
            )
            r_del = urllib.request.urlopen(req_del, timeout=5)
            check("DELETE /knowledge (nonexistent)", {"200"}, str(r_del.status), good, fail)
        except urllib.error.HTTPError as e:
            check("DELETE /knowledge (nonexistent)", {"200", "500"}, str(e.code), good, fail)

        # === INFRA ===
        print("\n=== INFRASTRUCTURE ===")
        r9 = urllib.request.urlopen("http://127.0.0.1:8000/openapi.json", timeout=5)
        check("OpenAPI", {"200"}, str(r9.status), good, fail)

        r10 = urllib.request.urlopen("http://127.0.0.1:8000/docs", timeout=5)
        check("Swagger UI", {"200"}, str(r10.status), good, fail)

    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        fail[0] += 1

    proc.terminate()
    proc.wait()

    print(f"\n=== RESULTS: {good[0]} passed, {fail[0]} failed ===")
    if fail[0] == 0:
        print("ALL TESTS PASSED")
    else:
        print(f"{fail[0]} TEST(S) FAILED")

    return 0 if fail[0] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
