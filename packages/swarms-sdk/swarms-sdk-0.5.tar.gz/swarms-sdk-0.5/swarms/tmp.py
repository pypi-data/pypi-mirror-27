from sdk import services

config = lambda: None
config.base_url = 'http://localhost:9040/'
config.username = 'ash.ketchum@alabastia.pkm'
config.password = 'pickachu'

campaigns, jobs, tasks, results = services.get(config)

c = campaigns.get(12)
print(c["name"])
js = campaigns.get_all_jobs(c)
for job in js:
    print(job["name"])
