# -*- coding: utf-8 -*-
import user_agent


class RandomUserAgentMiddleware(object):
	def process_request(self, request, spider):
		userAgent = user_agent.generate_user_agent()
		request.headers.setdefault("User-Agent", userAgent)
