package helpers

import (
	"net/url"
	"regexp"
)

type SourceType int

const (
	YOUTUBE_URL SourceType = 1 << iota
	COMMON_URL
	ITS_NOT_A_URL
)

func GetURLType(s string) SourceType {
	if isYouTubeURL(s) {
		return YOUTUBE_URL
	} else if isURL(s) {
		return COMMON_URL
	} 

	return ITS_NOT_A_URL
}

func isYouTubeURL(s string) bool {
	re := regexp.MustCompile(`^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+`)
	return re.MatchString(s)
}

func isURL(s string) bool {
    u, err := url.Parse(s)
    if err != nil || u.Scheme == "" || u.Host == "" {
        return false
    }
    return true
}