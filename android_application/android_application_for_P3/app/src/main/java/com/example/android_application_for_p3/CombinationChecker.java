package com.example.android_application_for_p3;

public class CombinationChecker {
    //Used to translate the received number into the corresponding combination
    private String[] possibleCombinations = {"HIGH CARD", "PAIR", "TWO PAIRS", "THREE OF A KIND",
            "STRAIGHT", "FLUSH", "FULL HOUSE", "FOUR OF A KIND", "STRAIGHT FLUSH", "ROYAL FLUSH"};

    private int cardAmount; // this is used to see how many cards make up the given combination
    private String currentCombination; //The name of the current combination
    private String[] currentCards; // The signatures of the cards in the combination
    private String combinationText; // combination text which should look like "6 5S 6C 7S 8H 9D 2254"
    // this means: "combination number - cards - rank

    CombinationChecker(String combinationText){
        this.combinationText = combinationText;
        readString(combinationText);

    }

    private void readString (String text){
        //splitting the received array up for each space
        String[] array = text.split(" ");

        //Finding the corresponding combination name from a list of names in order
        currentCombination = possibleCombinations[Integer.valueOf(array[0])];

        //setting the amount of cards based on how many cards were sent
        cardAmount = array.length - 2;

        //initializing the array with a length, so that we can add elements to it
        currentCards = new String[cardAmount];

        for (int i = 0; i < cardAmount; i++){
            //Saving the current cards on separate list
            currentCards[i] = array[i+1]; //we add one for the array, since the first element is the combo
        }
    }


    //--------------------------------------------//
    //-------------- GETTERS ----------------//

    public int getCardAmount() {
        return cardAmount;
    }

    public String getCurrentCombination() {
        return currentCombination;
    }

    public String[] getCurrentCards() {
        return currentCards;
    }

}
