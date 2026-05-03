import pytest
from unittest.mock import patch, MagicMock
from services.scraper_service import scrape_live_election_news, search_constituency_data

def test_search_constituency_found():
    """Test that existing constituency data is returned correctly."""
    result = search_constituency_data("Lucknow")
    assert result["found"] is True
    assert result["data"]["name"] == "Lucknow"

def test_search_constituency_not_found():
    """Test that missing constituency data returns a friendly message."""
    result = search_constituency_data("NonExistentCity")
    assert result["found"] is False
    assert "Data for" in result["message"]

@patch('requests.get')
def test_scrape_news_mocked(mock_get):
    """Test news scraping with a mocked response."""
    # Mocking the RSS XML response
    mock_response = MagicMock()
    mock_response.content = b"""
    <rss version="2.0">
        <channel>
            <item>
                <title>Election News 1</title>
                <link>http://example.com/1</link>
                <pubDate>Sat, 02 May 2026 12:00:00 GMT</pubDate>
                <source>Source 1</source>
            </item>
        </channel>
    </rss>
    """
    mock_get.return_value = mock_response
    
    news = scrape_live_election_news("en")
    assert len(news) == 1
    assert news[0]["title"] == "Election News 1"
    assert news[0]["source"] == "Source 1"
