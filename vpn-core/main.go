package main

import (
	"log"
	"vpn-core/proxy"
)

func main() {
	log.Println("Starting Adaptive Behavioral Stealth VPN Core...")
	
	// Слушаем на локальном порту 8080.
	// Весь трафик, приходящий сюда, будет проксироваться на тестовый хост (например, example.com)
	listenAddr := "127.0.0.1:8080"
	targetAddr := "google.com:80" // Тестовый IP-адрес google.com

	p := proxy.NewProxy(listenAddr, targetAddr)
	log.Fatalf("Proxy failed: %v", p.Start())
}
