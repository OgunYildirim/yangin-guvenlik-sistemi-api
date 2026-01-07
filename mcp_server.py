#!/usr/bin/env python3
"""
Yangın Risk Hesaplama MCP Servisi
Bu servis yangın risk skorunu hesaplar ve hava durumu verilerini kullanır.
"""

import asyncio
import json
import requests
from typing import Any
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# MCP Server oluştur
server = Server("yangin-risk-mcp")

# Public API - OpenWeatherMap alternatifi olarak Open-Meteo (ücretsiz, API key gerektirmez)
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

def get_weather_data(latitude: float, longitude: float) -> dict:
    """
    Public API kullanarak hava durumu verilerini çeker.
    Open-Meteo API - Ücretsiz, API key gerektirmez
    
    Args:
        latitude: Enlem
        longitude: Boylam
    
    Returns:
        Sıcaklık, nem ve rüzgar hızı bilgileri
    """
    try:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
            "timezone": "auto"
        }
        
        response = requests.get(WEATHER_API_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        current = data.get("current", {})
        
        return {
            "temperature": current.get("temperature_2m", 0),
            "humidity": current.get("relative_humidity_2m", 0),
            "wind_speed": current.get("wind_speed_10m", 0),
            "success": True
        }
    except Exception as e:
        return {
            "error": str(e),
            "success": False
        }

def calculate_fire_risk(
    temperature: float,
    humidity: float,
    wind_speed: float,
    building_type: str = "residential",
    has_fire_system: bool = True
) -> dict:
    """
    Yangın risk skorunu hesaplar.
    
    Args:
        temperature: Sıcaklık (°C)
        humidity: Nem oranı (%)
        wind_speed: Rüzgar hızı (km/h)
        building_type: Bina tipi (residential, commercial, industrial)
        has_fire_system: Yangın söndürme sistemi var mı?
    
    Returns:
        Risk skoru ve detaylar
    """
    # Temel risk skoru (0-100)
    risk_score = 0
    
    # Sıcaklık faktörü (30°C üzeri yüksek risk)
    if temperature > 35:
        risk_score += 30
    elif temperature > 30:
        risk_score += 20
    elif temperature > 25:
        risk_score += 10
    
    # Nem faktörü (düşük nem = yüksek risk)
    if humidity < 30:
        risk_score += 25
    elif humidity < 50:
        risk_score += 15
    elif humidity < 70:
        risk_score += 5
    
    # Rüzgar faktörü (yüksek rüzgar = yüksek risk)
    if wind_speed > 40:
        risk_score += 20
    elif wind_speed > 25:
        risk_score += 15
    elif wind_speed > 15:
        risk_score += 10
    
    # Bina tipi faktörü
    building_factors = {
        "residential": 5,
        "commercial": 10,
        "industrial": 20
    }
    risk_score += building_factors.get(building_type.lower(), 5)
    
    # Yangın sistemi varsa risk azalır
    if has_fire_system:
        risk_score = int(risk_score * 0.6)  # %40 risk azaltma
    
    # Risk seviyesi belirleme
    if risk_score >= 70:
        risk_level = "CRITICAL"
        recommendation = "Acil önlem alınmalı! Yangın riski çok yüksek."
    elif risk_score >= 50:
        risk_level = "HIGH"
        recommendation = "Dikkatli olunmalı. Yangın önlemleri gözden geçirilmeli."
    elif risk_score >= 30:
        risk_level = "MODERATE"
        recommendation = "Normal önlemler yeterli. Rutin kontroller yapılmalı."
    else:
        risk_level = "LOW"
        recommendation = "Risk düşük. Standart güvenlik protokolleri uygulanmalı."
    
    return {
        "risk_score": min(risk_score, 100),
        "risk_level": risk_level,
        "recommendation": recommendation,
        "factors": {
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "building_type": building_type,
            "has_fire_system": has_fire_system
        }
    }

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """
    MCP Tool'ları listeler.
    """
    return [
        Tool(
            name="calculate_fire_risk",
            description="Yangın risk skorunu hesaplar. Sıcaklık, nem, rüzgar hızı gibi faktörleri kullanarak 0-100 arası risk skoru verir.",
            inputSchema={
                "type": "object",
                "properties": {
                    "temperature": {
                        "type": "number",
                        "description": "Sıcaklık (°C)"
                    },
                    "humidity": {
                        "type": "number",
                        "description": "Nem oranı (%)"
                    },
                    "wind_speed": {
                        "type": "number",
                        "description": "Rüzgar hızı (km/h)"
                    },
                    "building_type": {
                        "type": "string",
                        "description": "Bina tipi: residential, commercial, industrial",
                        "enum": ["residential", "commercial", "industrial"]
                    },
                    "has_fire_system": {
                        "type": "boolean",
                        "description": "Yangın söndürme sistemi var mı?"
                    }
                },
                "required": ["temperature", "humidity", "wind_speed"]
            }
        ),
        Tool(
            name="get_weather_fire_risk",
            description="Belirtilen konum için hava durumu verilerini çeker ve yangın risk skorunu hesaplar. Public API kullanır.",
            inputSchema={
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "number",
                        "description": "Enlem (örn: 41.0082 - İstanbul)"
                    },
                    "longitude": {
                        "type": "number",
                        "description": "Boylam (örn: 28.9784 - İstanbul)"
                    },
                    "building_type": {
                        "type": "string",
                        "description": "Bina tipi: residential, commercial, industrial",
                        "enum": ["residential", "commercial", "industrial"]
                    },
                    "has_fire_system": {
                        "type": "boolean",
                        "description": "Yangın söndürme sistemi var mı?"
                    }
                },
                "required": ["latitude", "longitude"]
            }
        ),
        Tool(
            name="add_numbers",
            description="İki sayıyı toplar. Basit bir matematik işlemi örneği.",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "İlk sayı"
                    },
                    "b": {
                        "type": "number",
                        "description": "İkinci sayı"
                    }
                },
                "required": ["a", "b"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """
    MCP Tool çağrılarını işler.
    """
    if name == "add_numbers":
        # Basit toplama işlemi
        a = arguments.get("a", 0)
        b = arguments.get("b", 0)
        result = a + b
        
        return [
            TextContent(
                type="text",
                text=json.dumps({
                    "result": result,
                    "operation": f"{a} + {b} = {result}"
                }, indent=2, ensure_ascii=False)
            )
        ]
    
    elif name == "calculate_fire_risk":
        # Yangın risk hesaplama
        temperature = arguments.get("temperature", 20)
        humidity = arguments.get("humidity", 50)
        wind_speed = arguments.get("wind_speed", 10)
        building_type = arguments.get("building_type", "residential")
        has_fire_system = arguments.get("has_fire_system", True)
        
        result = calculate_fire_risk(
            temperature, humidity, wind_speed, building_type, has_fire_system
        )
        
        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )
        ]
    
    elif name == "get_weather_fire_risk":
        # Hava durumu + yangın risk hesaplama (Public API kullanımı)
        latitude = arguments.get("latitude")
        longitude = arguments.get("longitude")
        building_type = arguments.get("building_type", "residential")
        has_fire_system = arguments.get("has_fire_system", True)
        
        if latitude is None or longitude is None:
            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "error": "Latitude ve longitude parametreleri gerekli"
                    }, ensure_ascii=False)
                )
            ]
        
        # Public API'den hava durumu verilerini çek
        weather_data = get_weather_data(latitude, longitude)
        
        if not weather_data.get("success"):
            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "error": "Hava durumu verileri alınamadı",
                        "details": weather_data.get("error")
                    }, ensure_ascii=False)
                )
            ]
        
        # Yangın risk skorunu hesapla
        risk_result = calculate_fire_risk(
            temperature=weather_data["temperature"],
            humidity=weather_data["humidity"],
            wind_speed=weather_data["wind_speed"],
            building_type=building_type,
            has_fire_system=has_fire_system
        )
        
        # Sonuçları birleştir
        result = {
            "location": {
                "latitude": latitude,
                "longitude": longitude
            },
            "weather": {
                "temperature": weather_data["temperature"],
                "humidity": weather_data["humidity"],
                "wind_speed": weather_data["wind_speed"]
            },
            "fire_risk": risk_result
        }
        
        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )
        ]
    
    else:
        return [
            TextContent(
                type="text",
                text=json.dumps({
                    "error": f"Bilinmeyen tool: {name}"
                }, ensure_ascii=False)
            )
        ]

async def main():
    """MCP Server'ı başlatır."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="yangin-risk-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
