def test_upload_grant_and_confirm(client, fake_messages_collection):
    # Grant
    grant_resp = client.post("/uploads/grant", json={
        "filename": "pic.png",
        "mimetype": "image/png",
        "size": 1024 * 100
    })
    assert grant_resp.status_code == 200
    grant = grant_resp.json()
    assert "key" in grant and "putUrl" in grant

    # Confirm
    confirm_resp = client.post("/uploads/confirm", json={
        "key": grant["key"],
        "filename": "pic.png",
        "mimetype": "image/png",
        "author": "u1"
    })
    assert confirm_resp.status_code == 200
    data = confirm_resp.json()
    assert data["ok"] is True
    assert data["message"]["attachment"]["filename"] == "pic.png"
    # deve ter sido salvo em memória
    assert any(
        doc.get("attachment", {}).get("filename") == "pic.png"
        for doc in fake_messages_collection.data
    )
