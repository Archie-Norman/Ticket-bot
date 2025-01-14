const puppeteer = require('puppeteer');

const userCredentials = [
//    {username: "sexy.note@gmail.com", password: "wag1winebar"},
  //  {username: "solo.else@gmail.com", password: "wag1winebar"},
    {username: "jury.foam@gmail.com", password: "wag1winebar"}
];
async function runPuppeteerScript(username, password) {
    const browser = await puppeteer.launch({
        headless: false, // Keep it true for headless mode
        args: [
            '--no-sandbox', // May improve speed, but less secure
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--disable-gpu',
            '--no-zygote',
        ],
        defaultViewport: null, // Set default viewport to null to allow Puppeteer to maximize the window
    });


    const page = await browser.newPage();


    try {
        await page.setRequestInterception(true);
        await page.setCacheEnabled(false); // Disable caching

        page.on('request', interceptedRequest => {
            const resourceType = interceptedRequest.resourceType();
            if (resourceType === 'image' || resourceType === 'stylesheet') {
                interceptedRequest.abort();
            } else {
                interceptedRequest.continue();
            }
        });  
        

        await page.goto("https://fixr.co/login", { waitUntil: 'domcontentloaded' });  // Emulate keyboard shortcut to zoom out the page
        

        await page.waitForSelector('#login-email', { visible: true });
        await page.type('#login-email', username);
        await page.type('#login-password', password);

        await page.evaluate(() => {
            // Find the button based on its class and text content
            const buttons = document.querySelectorAll('button.sc-d03939e3-0.eaVubj');
            
            // Loop through all found buttons
            buttons.forEach(button => {
                // Check if the button contains the text 'Confirm'
                if (button.querySelector('span.sc-d03939e3-1.bqyvLM')?.textContent === 'Confirm') {
                    // Click the button
                    button.click();
                    console.timeEnd("timer end"); // Stop the timer when the button is clicked
                }
            });
        });
        
        await page.click('button.sc-d03939e3-0.eaVubj > span.sc-d03939e3-1.bqyvLM');

        await page.waitForNavigation();

        await new Promise(resolve => setTimeout(resolve, 1000));
        
        console.time(username);
        await page.goto("https://fixr.co/event/end-of-exams-blow-out-tickets-699990525/tickets", { waitUntil: 'domcontentloaded' });  

            
        await page.waitForSelector('.sc-131cfbab-0');
  
        const elcount = await page.evaluate(() => {
          return document.querySelectorAll('.sc-7929a83f-0').length;
        });
        
        console.log('Number of elements with class:', elcount);
        
        
        let elementCount = 0;
        while (elementCount < 3) {
            // Reload the page and wait for the specified selector
            await page.reload({ waitUntil: 'domcontentloaded' });
            await page.waitForSelector('.sc-131cfbab-0'); // Wait for the specified selector
        
            // Evaluate the element count
            elementCount = await page.evaluate(() => {
                return document.querySelectorAll('.sc-7929a83f-0').length;
            });
        
            console.log('Number of elements with class:', elementCount);
        
            // If the count is below 4, log a message and continue the loop
            if (elementCount < 3) {
                console.log("Element count is below 4. Refreshing page...");
            }
        }
        
        console.log("Element count is now equal to or more than 4. Continuing with the script...");
        
        
        

        
        // Evaluate and click the second button inside the second div with class sc-7929a83f-0
        await page.evaluate(() => {
            // Select the second div with class sc-7929a83f-0
            const divs = document.querySelectorAll('.sc-7929a83f-0');
            
            // Check if there are at least 2 divs with the specified class
            if (divs.length >= 2) {
                const secondDiv = divs[2]; // 0 is 8-830 ticket
                
                // Find all buttons inside the second div
                const buttons = secondDiv.querySelectorAll('button[type="button"]');
                if (buttons.length >= 2) { // Ensure there are at least 2 buttons
                    buttons[1].click(); // Click the second button (index 1)
                } else {
                    console.log('Not enough buttons inside the second div.');
                }
            } else {
                console.log('Not enough divs with the specified class.');
            }
        });       
        
        let reserveButtonFound = false; // Declare and initialize the flag outside the loop

        while (!reserveButtonFound) {
            try {
                await page.waitForSelector('button.sc-d03939e3-0.eaVubj > span.sc-d03939e3-1.bqyvLM', { timeout: 1000 });
                const buttons = await page.$$('button.sc-d03939e3-0.eaVubj');
                for (const button of buttons) {
                    const buttonText = await page.evaluate(element => element.querySelector('span.sc-d03939e3-1.bqyvLM')?.textContent, button);
                    if (buttonText === 'Reserve') {
                        await button.click();
                        reserveButtonFound = false; // Reset the flag to keep searching for the button
                        console.timeEnd(username); // End the timer when the button is clicked
                        break; // Exit the loop since button is found
                    }
                }
            } catch (error) {
                console.error("Reserve button not found:", error);
                reserveButtonFound = true; // Set flag to true to indicate button was not found
                console.timeEnd(username); // End the timer if the button is not found
            }
        }
        
        
        
        
        await new Promise(resolve => setTimeout(resolve, 1000));

        await page.evaluate(() => {
            document.querySelector("#ticket-protection-no").click();
        });
        

        
        await new Promise(resolve => setTimeout(resolve, 2000));  
        

        await page.click('button.sc-d03939e3-0.eaVubj[style*="--background: #cc013e; --color: #ffffff; --borderColor: transparent; --padding: 14px 24px; --fontSize: 14px;"]');

      
        await new Promise(resolve => setTimeout(resolve, 2000));  

        const buttonsCount = await page.$$eval('button.sc-d03939e3-0.eaVubj[style*="--background: #cc013e; --color: #ffffff; --borderColor: transparent; --padding: 14px 24px; --fontSize: 14px; width: 100%;"]', buttons => buttons.length);
        console.log("Number of buttons:", buttonsCount);
        
        

   //     await page.click('button.sc-d03939e3-0.eaVubj[style*="--background: #cc013e; --color: #ffffff; --borderColor: transparent; --padding: 14px 24px; --fontSize: 14px; width: 100%;"]');


    } catch (error) {
        console.error("Error occurred:", error);

    }
}

(async () => {
    const promises = userCredentials.map(cred => runPuppeteerScript(cred.username, cred.password));
    await Promise.all(promises);
})();
