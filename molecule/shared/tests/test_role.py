def test_pmm_server_container(host):
    container = host.docker("pmm-server")
    assert container.name == "pmm-server"
    assert container.is_running


def test_pmm_data_volume(host):
    result = host.run("docker volume inspect pmm-data")
    assert result.rc == 0
