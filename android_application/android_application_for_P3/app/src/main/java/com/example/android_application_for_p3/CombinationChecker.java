package com.example.android_application_for_p3;

import java.util.LinkedList;

public class CombinationChecker {
    //Used to translate the received number into the corresponding combination
    private String[] possibleCombinations = {"HIGH CARD", "PAIR", "TWO PAIRS", "THREE OF A KIND",
            "STRAIGHT", "FLUSH", "FULL HOUSE", "FOUR OF A KIND", "STRAIGHT FLUSH", "ROYAL FLUSH"};

    private int cardAmount; // this is used to see how many cards make up the given combination
    private String currentCombination; //The name of the current combination
    //private String[] currentCards; // The signatures of the cards in the combination

    LinkedList<String> currentCards = new LinkedList<>();

    CombinationChecker(String combinationText){
        // combination text should look like "6 5S6C7S8H9D 2254"
        // this means: "combination number - cards - rank
        readString(combinationText);
    }

    private void readString (String text){
        //splitting the received array up for each space
        String[] array = text.split(" ");

        //Finding the corresponding combination name from a list of names in order
        currentCombination = possibleCombinations[Integer.valueOf(array[0])];
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
