package com.eyagassab.lumina.data.remote;

import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public final class RetrofitClient {

    // 10.0.2.2 est l'alias spécial de l'émulateur Android vers localhost de la machine hôte
    private static final String BASE_URL = "http://127.0.0.1:8000/";

    private static volatile LuminaApiService instance;

    private RetrofitClient() {
        // Empêche l'instanciation directe
    }

    public static LuminaApiService getApiService() {
        if (instance == null) {
            synchronized (RetrofitClient.class) {
                if (instance == null) {
                    Retrofit retrofit = new Retrofit.Builder()
                            .baseUrl(BASE_URL)
                            .addConverterFactory(GsonConverterFactory.create())
                            .build();
                    instance = retrofit.create(LuminaApiService.class);
                }
            }
        }
        return instance;
    }
}