package com.eyagassab.lumina.data.remote;

import retrofit2.Call;
import retrofit2.http.GET;

public interface LuminaApiService {

    @GET("api/daily")
    Call<DailyConceptsResponseDto> getDailyConcepts();
}