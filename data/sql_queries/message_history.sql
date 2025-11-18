select 
	msg."key",
	msg."message" ->> 'conversation'
from "Instance" as ins
inner join "Message" as msg
	on msg."instanceId" = ins."id"
where msg."key" ->> 'remoteJid' = %(remoteJid)s
	and ins."name" = %(instance)s