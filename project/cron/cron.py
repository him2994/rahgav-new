from plan import Plan

cron = Plan()

cron.command('python script.py', every='1.minute')
# cron.script('script.py', every='1.day', path='/web/yourproject/scripts',
                         # environment={'YOURAPP_ENV': 'production'})

# if __name__ == "__main__":
cron.run(run_type='write')
