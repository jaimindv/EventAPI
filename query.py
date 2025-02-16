sql_query = """
SELECT t.event_id, e.name, SUM(t.quantity) AS total_tickets_sold
FROM public.event_ticket AS t
LEFT OUTER JOIN public.event_event AS e
ON t.event_id = e.id
GROUP BY (t.event_id, e.name)
ORDER BY total_tickets_sold DESC
LIMIT 3;
"""
