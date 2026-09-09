// ========================================
// AARAVVERSE ADMIN PANEL JAVASCRIPT
// ========================================

document.addEventListener("DOMContentLoaded", function () {

    // ========================================
    // ELEMENTS
    // ========================================

    const subjectSelect = document.getElementById("subject");
    const chapterSelect = document.getElementById("chapter");
    const contentTypeSelect = document.getElementById("content_type");

    // Check elements
    console.log("Subject:", subjectSelect);
    console.log("Chapter:", chapterSelect);
    console.log("Content:", contentTypeSelect);


    // ========================================
    // CHAPTER DATA
    // ========================================

    const chapters = {

        // PHYSICS
        physics: [
            ["1", "Electric Charges and Fields"],
            ["2", "Electrostatic Potential and Capacitance"],
            ["3", "Current Electricity"],
            ["4", "Moving Charges and Magnetism"],
            ["5", "Magnetism and Matter"],
            ["6", "Electromagnetic Induction"],
            ["7", "Alternating Current"],
            ["8", "Electromagnetic Waves"],
            ["9", "Ray Optics and Optical Instruments"],
            ["10", "Wave Optics"],
            ["11", "Dual Nature of Radiation and Matter"],
            ["12", "Atoms"],
            ["13", "Nuclei"],
            ["14", "Semiconductor Electronics"]
        ],

        // CHEMISTRY
        chemistry: [
            ["1", "Solutions"],
            ["2", "Electrochemistry"],
            ["3", "Chemical Kinetics"],
            ["4", "d and f Block Elements"],
            ["5", "Coordination Compounds"],
            ["6", "Haloalkanes and Haloarenes"],
            ["7", "Alcohols, Phenols and Ethers"],
            ["8", "Aldehydes, Ketones and Carboxylic Acids"],
            ["9", "Amines"],
            ["10", "Biomolecules"]
        ],

        // BIOLOGY
        biology: [
            ["1", "Sexual Reproduction in Flowering Plants"],
            ["2", "Human Reproduction"],
            ["3", "Reproductive Health"],
            ["4", "Principles of Inheritance and Variation"],
            ["5", "Molecular Basis of Inheritance"],
            ["6", "Evolution"],
            ["7", "Human Health and Disease"],
            ["8", "Microbes in Human Welfare"],
            ["9", "Biotechnology: Principles and Processes"],
            ["10", "Biotechnology and its Applications"],
            ["11", "Organisms and Populations"],
            ["12", "Ecosystem"],
            ["13", "Biodiversity and Conservation"],
            ["14", "Environmental Issues"]
        ],

        // ENGLISH
        english: [
            ["1", "Flamingo"],
            ["2", "Vistas"]
        ],

        // COMPUTER SCIENCE
        "computer-science": [
            ["1", "Computer Networks"],
            ["2", "Database Management System"],
            ["3", "Data Structures"],
            ["4", "Python"],
            ["5", "Computer Security"]
        ],

        // PHYSICAL EDUCATION
        "physical-education": [
            ["1", "Management of Sporting Events"],
            ["2", "Children and Women in Sports"],
            ["3", "Yoga and Lifestyle"],
            ["4", "Physical Education and Sports for CWSN"],
            ["5", "Sports and Nutrition"],
            ["6", "Test and Measurement in Sports"],
            ["7", "Physiology and Sports"],
            ["8", "Biomechanics and Sports"],
            ["9", "Psychology and Sports"],
            ["10", "Training in Sports"]
        ]
    };


    // ========================================
    // LOAD CHAPTERS
    // ========================================

    function loadChapters(subject) {

        // Reset dropdown
        chapterSelect.innerHTML =
            '<option value="">Select Chapter</option>';

        // If subject doesn't have chapters
        if (!chapters[subject]) {
            return;
        }

        // Add chapters
        chapters[subject].forEach(function (chapter) {

            const option = document.createElement("option");

            option.value = chapter[0];

            option.textContent =
                "Chapter " +
                chapter[0] +
                " — " +
                chapter[1];

            chapterSelect.appendChild(option);
        });

        console.log(
            "Loaded chapters for:",
            subject
        );
    }


    // ========================================
    // SUBJECT CHANGE
    // ========================================

    if (subjectSelect) {

        subjectSelect.addEventListener(
            "change",
            function () {

                loadChapters(this.value);

            }
        );
    }


    // ========================================
    // CONTENT TYPE
    // ========================================

    function updateChapterVisibility() {

        const contentType = contentTypeSelect.value;

        if (
            contentType === "homework" ||
            contentType === "important"
        ) {

            // Hide chapter
            chapterSelect.style.display = "none";

            // Not required
            chapterSelect.required = false;

            // Clear chapter
            chapterSelect.value = "";

        } else {

            // Show chapter
            chapterSelect.style.display = "block";

            // Required
            chapterSelect.required = true;
        }
    }


    // ========================================
    // CONTENT TYPE CHANGE
    // ========================================

    if (contentTypeSelect) {

        contentTypeSelect.addEventListener(
            "change",
            updateChapterVisibility
        );

    }


    // ========================================
    // INITIAL STATE
    // ========================================

    updateChapterVisibility();


    // ========================================
    // PHOTO INPUT
    // ========================================

    const photoInput =
        document.querySelector('input[name="photo"]');

    if (photoInput) {

        photoInput.addEventListener(
            "change",
            function () {

                if (this.files.length > 0) {

                    console.log(
                        "Selected photo:",
                        this.files[0].name
                    );

                }

            }
        );

    }


    // ========================================
    // LOADED
    // ========================================

    console.log(
        "AaravVerse Admin Panel loaded successfully."
    );

});