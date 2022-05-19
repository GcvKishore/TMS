function enableSectionEdit() {
    let viewElements = document.getElementsByClassName('view_section')
    for (let i = 0; i < viewElements.length; i++) {
        viewElements[i].disabled = true;
        viewElements[i].hidden = true;
    }

    let editElements = document.getElementsByClassName('edit_section')
    for (let i = 0; i < editElements.length; i++) {
        editElements[i].disabled = false;
        editElements[i].hidden = false;
    }
}

function addDescription() {
    document.getElementById('addSectionDescription').disabled = false
    document.getElementById('addSectionDescription').hidden = false
    document.getElementById('removeDescriptionBtn').hidden = false
    document.getElementById('addDescriptionBtn').hidden = true
    document.getElementById('id_description').setAttribute("name", "description")
}

function removeDescription() {
    document.getElementById('addSectionDescription').disabled = true
    document.getElementById('addSectionDescription').hidden = true
    document.getElementById('removeDescriptionBtn').hidden = true
    document.getElementById('addDescriptionBtn').hidden = false
    document.getElementById('id_description').setAttribute("name", "description_not")
}

function addInstructions() {
    document.getElementById('addSectionInstructions').disabled = false
    document.getElementById('addSectionInstructions').hidden = false
    document.getElementById('removeInstructionsBtn').hidden = false
    document.getElementById('addInstructionsBtn').hidden = true
    document.getElementById('id_instructions').setAttribute("name", "instructions")
}

function removeInstructions() {
    document.getElementById('addSectionInstructions').disabled = true
    document.getElementById('addSectionInstructions').hidden = true
    document.getElementById('removeInstructionsBtn').hidden = true
    document.getElementById('addInstructionsBtn').hidden = false
    document.getElementById('id_instructions').setAttribute("name", "instructions_not")
}
