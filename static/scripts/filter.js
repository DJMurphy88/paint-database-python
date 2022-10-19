function listFilter() {
    var input, filter, cards, card, i, txtValue;
    var name, id, colour, type, pots, brand, status;

    input = document.getElementById("userInput");
    filter = input.value.toUpperCase();
    cards = document.getElementsByClassName("fullCard")

    for (i = 0; i < cards.length; i++) {
        card = cards[i];
        console.log(card)
        if (card) {
            txtValue = card.textContent || card.innerText;
            txtValue.trim();

            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                console.log("- match")
                cards[i].style.display = "";
            }
            else {
                console.log("- no match")
                cards[i].style.display = "none";
            }
        }
    }
}
