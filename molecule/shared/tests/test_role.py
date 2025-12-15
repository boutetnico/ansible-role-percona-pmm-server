import json


def test_pmm_server_container(host):
    container = host.docker("pmm-server")
    assert container.name == "pmm-server"
    assert container.is_running


def test_pmm_server_container_image(host):
    result = host.run("docker inspect pmm-server --format '{{.Config.Image}}'")
    assert result.rc == 0
    assert "percona/pmm-server" in result.stdout


def test_pmm_data_volume(host):
    result = host.run("docker volume inspect pmm-data")
    assert result.rc == 0


def test_pmm_data_volume_mount(host):
    result = host.run("docker inspect pmm-server --format '{{json .Mounts}}'")
    assert result.rc == 0
    mounts = json.loads(result.stdout)
    volume_mount = next((m for m in mounts if m["Name"] == "pmm-data"), None)
    assert volume_mount is not None
    assert volume_mount["Destination"] == "/srv"


def test_pmm_server_ports(host):
    result = host.run(
        "docker inspect pmm-server --format '{{json .NetworkSettings.Ports}}'"
    )
    assert result.rc == 0
    ports = json.loads(result.stdout)
    assert "8080/tcp" in ports
    assert "8443/tcp" in ports


def test_pmm_server_restart_policy(host):
    result = host.run(
        "docker inspect pmm-server --format '{{.HostConfig.RestartPolicy.Name}}'"
    )
    assert result.rc == 0
    assert result.stdout.strip() == "unless-stopped"


def _get_pmm_server_ip(host):
    """Get PMM server container IP address."""
    result = host.run(
        "docker inspect pmm-server "
        "--format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'"
    )
    return result.stdout.strip()


def test_pmm_server_healthcheck(host):
    # Health check endpoint should be accessible without auth
    # Retry up to 30 times (30 seconds) for PMM server to be ready
    pmm_ip = _get_pmm_server_ip(host)
    result = host.run(
        f"curl -s -o /dev/null -w '%{{http_code}}' "
        f"--retry 30 --retry-delay 1 --retry-all-errors "
        f"http://{pmm_ip}:8080/v1/readyz"
    )
    assert result.rc == 0
    assert result.stdout == "200"


def test_pmm_server_auth_required(host):
    # API endpoint should require authentication
    pmm_ip = _get_pmm_server_ip(host)
    result = host.run(
        f"curl -s -o /dev/null -w '%{{http_code}}' http://{pmm_ip}:8080/v1/server/version"
    )
    assert result.rc == 0
    assert result.stdout == "401"


def test_pmm_server_authenticated_response(host):
    # With default credentials, API should return 200
    pmm_ip = _get_pmm_server_ip(host)
    result = host.run(
        f"curl -s -o /dev/null -w '%{{http_code}}' "
        f"-u admin:admin http://{pmm_ip}:8080/v1/server/version"
    )
    assert result.rc == 0
    assert result.stdout == "200"
