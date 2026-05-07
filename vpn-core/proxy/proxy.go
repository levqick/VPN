package proxy

import (
	"io"
	"log"
	"net"
	"vpn-core/obfuscator"
)

// Proxy структура для пересылки TCP трафика
type Proxy struct {
	listenAddr string
	targetAddr string
}

func NewProxy(listenAddr, targetAddr string) *Proxy {
	return &Proxy{listenAddr: listenAddr, targetAddr: targetAddr}
}

func (p *Proxy) Start() error {
	listener, err := net.Listen("tcp", p.listenAddr)
	if err != nil {
		return err
	}
	defer listener.Close()
	log.Printf("Proxy is listening on %s, forwarding to %s\n", p.listenAddr, p.targetAddr)

	for {
		clientConn, err := listener.Accept()
		if err != nil {
			log.Printf("Failed to accept connection: %v\n", err)
			continue
		}
		go p.handleConnection(clientConn)
	}
}

func (p *Proxy) handleConnection(clientConn net.Conn) {
	defer clientConn.Close()
	log.Printf("New connection accepted from %s\n", clientConn.RemoteAddr())

	targetConn, err := net.Dial("tcp", p.targetAddr)
	if err != nil {
		log.Printf("Failed to connect to target: %v\n", err)
		return
	}
	defer targetConn.Close()

	// Оборачиваем соединения в наш Обфускатор (маскировщик)
	obfsClient := obfuscator.NewObfuscator(clientConn, "Client->Target")
	obfsTarget := obfuscator.NewObfuscator(targetConn, "Target->Client")

	// Пересылка данных в обе стороны
	go func() {
		io.Copy(targetConn, obfsClient)
	}()
	io.Copy(clientConn, obfsTarget)
}
