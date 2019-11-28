package com.example.android_application_for_p3;

import java.util.LinkedList;

public class CombinationChecker {
    //Used to translate the received number into the corresponding combination
    private String[] possibleCombinations = {"ROYAL FLUSH", "STRAIGHT FLUSH", "FOUR OF A KIND",
            "FULL HOUSE", "FLUSH", "STRAIGHT", "THREE OF A KIND", "TWO PAIRS", "PAIR", "HIGH CARD"};

    private int cardAmount; // this is used to see how many cards make up the given combination
    private String currentCombination; //The name of the current combination
    //private String[] currentCards; // The signatures of the cards in the combination

    LinkedList<String> currentCards = new LinkedList<>();
    int modeIndex = 0;

    CombinationChecker(String combinationText){
        // combination text should look like "6 5S6C7S8H9D 2254"
        // this means: "combination number - cards - rank
        readString(combinationText);
    }

    private void readString (String text){
        int modeThreshold = 5;
        String[] readCombinations = new String[modeThreshold]; //used to store the current combination before taking mode

        //splitting the received array up for each space
        String[] array = text.split(" ");

        //circling through spots in the array, to constantly update the mode
        if (modeIndex >= modeThreshold){
            modeIndex = 0;
        }

        //Finding the corresponding combination name from a list of names
        readCombinations[modeIndex] = possibleCombinations[Integer.valueOf(array[0])];

        //finding the the mode of the last five sent combinations
        int maxCounter = 0; //used to store the amount of cards in current mode
        for (int i = 0; i < modeThreshold; i++){ //checking though the stored combinations
            int counter = 0; // to count repetitions of current combination

            // circling through all saved combinations counting the matches
            for (int j = 0; j < modeThreshold; j++){
                if (readCombinations[i].equals(readCombinations[j])){
                    counter++;
                }
            }
            //Checking if the combination we just counted beats the current mode
            if (counter > maxCounter){
                maxCounter = counter;
                //saving the mode
                currentCombination = readCombinations[i];
            }
        }

        int i = 0;
        while(i < array[1].length()-1){
            String temp = String.valueOf(array[1].charAt(i+1)); //first
            temp += String.valueOf(array[1].charAt(i)); // plus second
            i += 2;
            currentCards.add(temp);
        }

        cardAmount = currentCards.size();
    }

    String cardNameToViewName(int index){
         // it could be like "6H", but need to make it to h6
        return currentCards.get(index).toLowerCase();
    }

    //--------------------------------------------//
    //-------------- GETTERS ----------------//

    public int getCardAmount() {
        return cardAmount;
    }

    public String getCurrentCombination() {
        return currentCombination;
    }

    public LinkedList<String> getCurrentCards() {
        return currentCards;
    }
}
