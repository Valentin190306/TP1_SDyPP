import requests
import time

BASE_URL = "http://localhost:8000"
NODO_D_IP = "127.0.0.1"
NODO_D_PORT = 8000


def test_health():
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200

    data = r.json()

    assert data["status"] == "ok"
    assert "uptime" in data
    assert "nodos_registrados" in data

    print("OK health")


def test_registro_primer_nodo():
    payload = {
        "ip": "127.0.0.1",
        "puerto": 5001
    }

    r = requests.post(f"{BASE_URL}/register", json=payload)

    assert r.status_code == 200
    data = r.json()

    assert data["nodos"] == []

    print("OK register first node")


def test_registro_segundo_nodo():
    payload = {
        "ip": "127.0.0.1",
        "puerto": 5002
    }

    r = requests.post(f"{BASE_URL}/register", json=payload)

    assert r.status_code == 200
    data = r.json()

    assert len(data["nodos"]) == 1
    assert data["nodos"][0]["puerto"] == 5001

    print("OK register second node")


def test_registro_invalido():
    payload = {
        "ip": "127.0.0.1"
    }

    r = requests.post(f"{BASE_URL}/register", json=payload)

    assert r.status_code == 400

    print("OK invalid register")


def run_tests():
    print("Iniciando tests del registry")

    time.sleep(1)

    test_health()
    test_registro_primer_nodo()
    test_registro_segundo_nodo()
    """test_registro_tercer_nodo()"""
    test_registro_invalido()
    test_health()


    print("Todos los tests pasaron")


if __name__ == "__main__":
    run_tests()