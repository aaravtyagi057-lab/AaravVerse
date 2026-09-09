/* SEARCH OVERLAY */

function openSearch() {

    const overlay =
        document.getElementById("searchOverlay");

    overlay.style.display = "flex";

    setTimeout(() => {
        document
            .getElementById("searchInput")
            .focus();
    }, 100);
}


function closeSearch() {

    document
        .getElementById("searchOverlay")
        .style.display = "none";

}


/* ESCAPE KEY */

document.addEventListener("keydown", function(event) {

    if (
        (event.ctrlKey || event.metaKey) &&
        event.key.toLowerCase() === "k"
    ) {

        event.preventDefault();

        openSearch();

    }


    if (event.key === "Escape") {

        closeSearch();

    }

});


/* SIMPLE SEARCH */

function searchSite() {

    const input =
        document
        .getElementById("searchInput")
        .value
        .toLowerCase()
        .trim();

    const results =
        document
        .getElementById("searchResults");


    if (input === "") {

        results.innerHTML = "";

        return;

    }


    const subjects = [

        {
            name: "Physics",
            link: "physics/index.html"
        },

        {
            name: "Chemistry",
            link: "chemistry/index.html"
        },

        {
            name: "Biology",
            link: "biology/index.html"
        },

        {
            name: "English",
            link: "english/index.html"
        },

        {
            name: "Computer Science",
            link: "computer-science/index.html"
        },

        {
            name: "Physical Education",
            link: "physical-education/index.html"
        }

    ];


    const found =
        subjects.filter(subject =>
            subject.name
            .toLowerCase()
            .includes(input)
        );


    if (found.length === 0) {

        results.innerHTML =
            "No results found 😭";

        return;

    }


    results.innerHTML =
        found.map(subject => `

            <a
                href="${subject.link}"
                style="
                    display:block;
                    padding:14px;
                    margin-top:8px;
                    border-radius:10px;
                    background:rgba(255,255,255,0.04);
                    color:white;
                    text-decoration:none;
                "
            >
                ${subject.name} →
            </a>

        `).join("");

}