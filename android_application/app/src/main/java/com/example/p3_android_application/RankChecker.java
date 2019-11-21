package com.example.p3_android_application;

public class RankChecker {

    int combinationRank; //rank of the combination, where 1 is Royal Flush and 7642 is worst possible
    int combinationAngle; // rank translated to the angle in the speedometer
    String combinationText; // combination text which should look like "6 5S 6C 7S 8H 9D 2254"
    // this means: "combination number - cards - rank

    RankChecker(String combinationText) {
        this.combinationText = combinationText;
        combinationRank = findRank(combinationText);
        combinationAngle = findAngle(combinationRank);
    }

    private int findRank (String text) {
        int rank;
        String[] array = text.split(" ");

        rank = Integer.parseInt(array[array.length - 1]);

        return rank;
    }

    private int findAngle (int rank){
        //calculating how many ranks fit into the same angle
        float degree = 7642/180;
        //Finding how many angles make up the rank
        float angle = rank/degree;
        //rounding it to a whole angle, since you won't be able to see the small changes
        return Math.round(angle);
    }
//--------------------------------------------//
    //-------------- GETTERS ----------------//

    public int getCombinationRank() {
        return combinationRank;
    }


    public int getCombinationAngle() {
        return combinationAngle;
    }
}