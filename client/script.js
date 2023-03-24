buy = document.querySelectorAll(".buy-btn")

buy.forEach(element => {
    element.addEventListener('click', async () => {

        try {
            loc = window.location.href

            console.log(loc)

            res = await fetch("http://localhost:5000/user/user1/buy/game6")

            if (res.status == 200) {

                data = await res.json()

                console.log(link)
                // mudar browser window
            }
        } catch (e) {
            console.log("Error fetching resources...")
        }

    })
});