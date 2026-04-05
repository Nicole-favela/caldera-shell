place test.sh inside of caldera folder.
open terminal and navigate to caldera folder
run chmod +x test.sh
if doesn't work do sudo chmod +x test.sh
to run script do ./test.sh
open caldera.log file which will be created and it say that new version are being created just reload it.
at the end you should see the following.
__________________________________________
2026-04-05 19:40:34 INFO     Creating new secure config in    config_util.py:102
                             conf/local.yml                                     
                    INFO                                       config_util.py:88
                             Log into Caldera with the                          
                             following admin credentials:                       
                                 Red:                                           
                                     USERNAME: red                              
                                     PASSWORD:                                  
                             5QYlRi0gJEeOl30cjKac_yKN8TRWohpdI                  
                             x2jjEPJUK8                                         
                                     API_TOKEN:                                 
                             xmTb4EIKoPPjxggIjhhAxQlPkApS4LUNv                  
                             2E0IsL0reE  S                                       
                                 Blue:                                          
                                     USERNAME: blue                             
                                     PASSWORD:                                  
                             qxyaMTXm_ZzBEUMveKl_Nx2WJRU8d8DoR                  
                             4EaNkBgbyo                                         
                                     API_TOKEN:                                 
                             p4XT7Ixv4SXBXT3m1GmVqTWmCoVXXHJ1F                  
                             XzwuMaJL_8                                         
                             To modify these values, edit the                   
                             conf/local.yml file and restart                    
                             Caldera.                                           
                    INFO     Using main config from conf/local.yml server.py:275
2026-04-05 19:40:36 INFO     Invalid Github Gist personal API contact_gist.py:70
                             token provided. Gist C2 contact                    
                             will not be started.                               
                    INFO     Generating temporary SSH private   tunnel_ssh.py:26
                             key. Was unable to use provided                    
                             SSH private key                                    
2026-04-05 19:40:37 INFO     Enabled plugin: training             app_svc.py:131
                    INFO     Enabled plugin: magma                app_svc.py:131
                    INFO     Enabled plugin: stockpile            app_svc.py:131
                    INFO     Enabled plugin: fieldmanual          app_svc.py:131
2026-04-05 19:40:38 INFO     Enabled plugin: debrief              app_svc.py:131
                    ERROR    Error importing plugin=builder, No   c_plugin.py:91
                             module named 'docker'                              
                    ERROR    Error loading plugin=builder,        c_plugin.py:59
                             'NoneType' object has no attribute                 
                             'description'                                      
                    INFO     Enabled plugin: manx                 app_svc.py:131
2026-04-05 19:40:46 INFO     Enabled plugin: atomic               app_svc.py:131
2026-04-05 19:40:47 INFO     Enabled plugin: compass              app_svc.py:131
                    INFO     Enabled plugin: access               app_svc.py:131
                    INFO     Enabled plugin: response             app_svc.py:131
2026-04-05 19:40:53 INFO     Enabled plugin: sandcat              app_svc.py:131
                    INFO     Creating SSH listener on 0.0.0.0,    logging.py:102
                             port 8022                                          
                    INFO     serving on 0.0.0.0:2222               server.py:741
                    WARNING  Unable to properly load .donut for  data_svc.py:468
                             payload                                            
                             plugins.stockpile.app.donut.donut_h                
                             andler due to failed import                        
2026-04-05 19:40:54 WARNING  upx does not meet the minimum        app_svc.py:191
                             version of 0.0.0. Upx is an optional               
                             dependency which adds more                         
                             functionality.                                     
2026-04-05 19:40:59 WARNING  Ability referenced in adversary   c_adversary.py:90
                             ef4d997c-a0d1-4067-9efa-87c58682d                  
                             b71 but not found:                                 
                             854e480af3b5e2946bb3ae44916e951a                   
                    WARNING  Ability referenced in adversary   c_adversary.py:90
                             ef4d997c-a0d1-4067-9efa-87c58682d                  
                             b71 but not found:                                 
                             23dafb943f2f1a3e21e8204826c7b271                   
2026-04-05 19:41:00 INFO     All systems ready.                    server.py:139

 ██████╗ █████╗ ██╗     ██████╗ ███████╗██████╗  █████╗
██╔════╝██╔══██╗██║     ██╔══██╗██╔════╝██╔══██╗██╔══██╗
██║     ███████║██║     ██║  ██║█████╗  ██████╔╝███████║
██║     ██╔══██║██║     ██║  ██║██╔══╝  ██╔══██╗██╔══██║
╚██████╗██║  ██║███████╗██████╔╝███████╗██║  ██║██║  ██║
 ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝

2026-04-05 19:41:08 INFO     Docs built successfully.                 hook.py:60

Once done you can access caldera on mozzila using local host and port 80
username will always be red, blue or admin
but passwords will all be different every time you run it.

NOTE: CALDERA IS STILL RUNNING IN THE BACKGROUND SO IF YOU WISH TO RERUN THIS SCRIPT PLEASE SHUT IT DOWN VIA SERVICES MANAGER.
