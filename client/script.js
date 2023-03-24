buy = document.querySelectorAll(".buy-btn")

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