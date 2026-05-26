from main import save_restaurants, load_restaurants
import main

def test_load_restaurants(tmp_path):
    main.DATA_FILE = tmp_path / "restaurants.json"
    result = load_restaurants()
    assert isinstance(result, list)

def test_save_restaurants(tmp_path):
    main.DATA_FILE = tmp_path / "restaurants.json"
    save_restaurants([{"id": 1, "name": "Test Cafe"}])
    assert main.DATA_FILE.exists()

def test_save_og_load_restaurants(tmp_path):
    main.DATA_FILE = tmp_path / "restaurants.json"
    data = [{"id": 1, "name": "Test Cafe"}]
    save_restaurants(data)
    result = load_restaurants()
    assert result[0]["name"] == "Test Cafe"