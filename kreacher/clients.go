package kreacher

import (
	"time"

	"github.com/redis/go-redis/v9"
	tele "gopkg.in/telebot.v3"
)

var rdb = redis.NewClient(&redis.Options{
	Addr:     "localhost:6379",
	Password: "", // no password set
	DB:       0,  // use default DB
	Protocol: 3,  // specify 2 for RESP 2 or 3 for RESP 3
})

var kbot, _ = tele.NewBot(tele.Settings{
	Token:  NewConfig().BotToken,
	Poller: &tele.LongPoller{Timeout: 10 * time.Second},
})
