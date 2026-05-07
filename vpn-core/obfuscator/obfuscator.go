package obfuscator

import (
	"encoding/json"
	"log"
	"net"
	"net/http"
	"time"
)

type Obfuscator struct {
	conn      net.Conn
	direction string
}

type MLResponse struct {
	Profile      string `json:"profile"`
	JitterMs     int    `json:"jitter_ms"`
	PaddingBytes int    `json:"padding_bytes"`
}

func NewObfuscator(conn net.Conn, direction string) *Obfuscator {
	return &Obfuscator{conn: conn, direction: direction}
}

// getMLPattern делает запрос к локальному Python API для получения "умной" задержки
func getMLPattern() (int, error) {
	// Для MVP запрашиваем паттерн "потоковое видео"
	resp, err := http.Get("http://127.0.0.1:5000/pattern?profile=video")
	if err != nil {
		return 0, err
	}
	defer resp.Body.Close()

	var mlResp MLResponse
	if err := json.NewDecoder(resp.Body).Decode(&mlResp); err != nil {
		return 0, err
	}
	return mlResp.JitterMs, nil
}

func (o *Obfuscator) Read(b []byte) (int, error) {
	n, err := o.conn.Read(b)
	if n > 0 {
		// Обращаемся к Python ИИ за величиной задержки
		jitterMs, mlErr := getMLPattern()
		if mlErr != nil {
			log.Printf("[Obfuscator %s] Ошибка связи с ИИ: %v. Базовая задержка 10мс.", o.direction, mlErr)
			jitterMs = 10
		}

		jitter := time.Duration(jitterMs) * time.Millisecond
		time.Sleep(jitter)
		log.Printf("[Obfuscator %s] Перехвачено %d байт. ИИ назначил задержку: %v\n", o.direction, n, jitter)
	}
	return n, err
}

func (o *Obfuscator) Write(b []byte) (int, error) {
	return o.conn.Write(b)
}

func (o *Obfuscator) Close() error {
	return o.conn.Close()
}
