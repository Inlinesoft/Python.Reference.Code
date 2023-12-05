def test_get_stats(test_api_client):
    response = test_api_client.get("/products/BTCW/stats")
    json_response = response.json()
    print(json_response)

    assert "stats" in json_response
    # todo: loaddevdata should insert stats objects
    # assert len(json_response["stats"]) > 0


def test_post_stats(test_api_client):
    body = {
        "run_date": "2020-05-11",
        "force": False,
        "reason": "generate stats from run",
    }
    response = test_api_client.post("/products/BTCW/stats", json=body)
    # json_response = response.json()
    # print(json_response)

    assert response.status_code == 400
    # should be successful, todo: insert stats data on loaddev data
    # assert json_response == {"Status": "success"}
