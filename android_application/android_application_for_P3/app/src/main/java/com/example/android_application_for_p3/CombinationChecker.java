package com.example.android_application_for_p3;

import java.util.Collections;
import java.util.Comparator;
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

        //splitting the received array up for each space
        String[] array = text.split(" ");

        currentCombination = possibleCombinations[Integer.valueOf(array[0])];
        System.out.println(currentCombination);

        int i = 0;
        while(i < array[1].length()-1){
            String temp = String.valueOf(array[1].charAt(i+1)); //first
            temp += String.valueOf(array[1].charAt(i)); // plus second
            i += 2;
            currentCards.add(temp);
        }
        sortCards();
        cardAmount = currentCards.size();
    }

    String cardNameToViewName(int index){
         // it could be like "6H", but need to make it to h6
        return currentCards.get(index).toLowerCase();
    }

    private void sortCards(){
        //could get like ["s2", "d6", "c8", "ct", "sa"]

        Collections.sort(currentCards, new Comparator<String>() {
            @Override
            public int compare(String o1, String o2) {
                return Character.compare(o1.charAt(1), o2.charAt(1));
            }
        });
        System.out.println(currentCards);
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
