package com.example.p3_android_application;

public class RankChecker {

    int combinationRank; //rank of the combination, where 1 is Royal Flush and 7642 is worst possible
    int combinationAngle; // rank translated to the angle in the speedometer
    String combinationText = ""; // combination text which should look like "straight 5S6C7S8H9D 2254"
                                            // this means: "combination name - cards - rank

    RankChecker(String combinationText){

    }

//--------------------------------------------//
    //-------------- GETTERS ----------------//

    public int getCombinationRank() {
        return combinationRank;
    }
}
