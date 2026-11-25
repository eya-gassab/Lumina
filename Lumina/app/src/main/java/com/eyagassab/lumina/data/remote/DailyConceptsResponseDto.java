package com.eyagassab.lumina.data.remote;

import com.google.gson.annotations.SerializedName;

import java.util.List;

public class DailyConceptsResponseDto {

    @SerializedName("date")
    private String date;

    @SerializedName("count")
    private int count;

    @SerializedName("concepts")
    private List<ConceptDto> concepts;

    public String getDate() {
        return date;
    }

    public int getCount() {
        return count;
    }

    public List<ConceptDto> getConcepts() {
        return concepts;
    }
}