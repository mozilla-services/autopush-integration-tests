E2E-TESTS
----------------------------

setting STAGE config to:
```dom.push.serverURL = autopush.stage.mozaws.net```

### DESKTOP E2E PUSH TEST

**setup:**  
start browser with new profile  
open: about:config  
set: dom.push.loglevel=debug (instead of 'off')  
open: Tools > WebDeveloper > BrowserConsole  
open: [https://mozilla-services.github.io/autopush-e2e-test/](https://mozilla-services.github.io/autopush-e2e-test/)  
choose: "service-worker.js"  
click: "register Service Worker"  
click: "subscribe to push"  
observe push registration in console  
click: "Always Receive Notifications" (in pop-up window)  

1. **registration test**

  **steps:**  :q
  
  click: "XHR to webpush app-server"   
  
  **observe:**   
  successful registration in console

2. **message delivery test**

  **setup:**  
  set: Repeat = 2  
  set: Delay (seconds) = 15  

  **steps:**  
  click: "XHR to webpush app-server"  
  observe: 2 pop notifications 15 seconds apart  
 
3. **payload test**

  **setup:**  
  set: Title = PAYLOAD TEST  
  set: Body = BODY TEXT HERE  
  set: TTL = 360  
  set: Repeat = 4  
  set: Delay (seconds): 20  

  **steps:**  
  click: "XHR to webpush app-server"  
  
  **observe:**  
  should see delayed pop notifications with Title, Body specified  

4. **storage test**

  **purpose:**
  verify that a request is stored on autopush for delayed delivery

  **setup:**  
  (same as 3 above)  

  **steps:  **  
  click: "XHR to webpush app-server    
  wait for pop notification, then immediately close browser    
  wait 25 seconds    
  re-open browser      
  
  **observe:**   
  should see 3 more delayed messages delivered on browser restart  
