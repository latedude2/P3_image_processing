package com.example.android_application_for_p3;

public class RankChecker {

    float MAX_COMBINATIONS = 7642;
    float MAX_ANGLE = 180;

    int combinationRank; //rank of the combination, where 1 is Royal Flush and 7642 is worst possible
    int combinationAngle; // rank translated to the angle in the speedometer
    String combinationText; // combination text which should look like "6 5S 6C 7S 8H 9D 2254"
    // this means: "combination number - cards - rank

    RankChecker(String combinationText) {
        this.combinationText = combinationText;
        combinationRank = findRank(combinationText);
        combinationAngle = findAngle(7643 - (float) combinationRank);
    }

    private int findRank (String text) {
        int rank;
        String[] array = text.split(" ");

        rank = Integer.parseInt(array[array.length - 1]);

        return rank;
    }

    private int findAngle (float rank){
        //calculating how many ranks fit into the same angle
        float degree = MAX_COMBINATIONS / MAX_ANGLE;
        //Finding how many angles make up the rank
        float angle = rank/degree;
        //rounding it to a whole angle, since you won't be able to see the small changes
        return Math.round(angle);
    }
//--------------------------------------------//
    //-------------- GETTERS ----------------//

    int getCombinationAngle() {
        return combinationAngle;
    }
}
