"""
Test StatusTable row ordering, updates, and rendering output.
"""
from crUPto.ui.status_table import StatusTable

def test_status_table_basic():
    table = StatusTable(columns=["Asset", "Status", "Amount"])
    table.set_row("BTC", ["BTC", "staking", "0.5"])
    table.set_row("ETH", ["ETH", "pending", "1.2"])
    out = table.render()
    assert "Asset" in out and "Status" in out and "Amount" in out
    assert "BTC" in out and "ETH" in out
    # Update row
    table.set_row("ETH", ["ETH", "staking", "2.0"])
    out2 = table.update()
    assert "2.0" in out2
    # Remove row
    table.remove_row("BTC")
    out3 = table.update()
    assert "BTC" not in out3

def test_status_table_order():
    table = StatusTable(columns=["Asset", "Status"], order=["ETH", "BTC"])
    table.set_row("BTC", ["BTC", "staking"])
    table.set_row("ETH", ["ETH", "pending"])
    lines = table._build_table()
    # ETH should come before BTC
    eth_idx = [i for i, l in enumerate(lines) if "ETH" in l][0]
    btc_idx = [i for i, l in enumerate(lines) if "BTC" in l][0]
    assert eth_idx < btc_idx

def test_status_table_as_text():
    table = StatusTable(columns=["Asset", "Status"])
    table.set_row("BTC", ["BTC", "staking"])
    txt = table.as_text()
    assert "BTC" in txt and "staking" in txt
