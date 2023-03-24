buy = document.querySelectorAll(".buy-btn")
trade = document.querySelectorAll(".buy-community-btn")

buy.forEach(element => {
    element.addEventListener('click', async () => {

        try {
            const loc = window.location.href

            console.log(loc)

            const res = await fetch("http://localhost:5000/user/user1/buy/game6", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "link": loc
                })
            })

            const data = await res.text()

            window.location = data 
        } catch (e) {
            console.log(e)
            console.log("Error fetching resources...")
        }

    })
});

trade.forEach(element => {
    element.addEventListener('click', async () => {

        try {
            const loc = window.location.href

            console.log(loc)

            const res = await fetch("http://localhost:5000/user/user2/buy/game6/other", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "link": loc
                })
            })

            const data = await res.text()

            window.location = data
        } catch (e) {
            console.log(e)
            console.log("Error fetching resources...")
        }

    })
});