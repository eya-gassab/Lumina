package com.eyagassab.lumina.data;

import android.content.Context;
import android.util.Log;

import androidx.lifecycle.LiveData;

import com.eyagassab.lumina.data.remote.ConceptDto;
import com.eyagassab.lumina.data.remote.DailyConceptsResponseDto;
import com.eyagassab.lumina.data.remote.LuminaApiService;
import com.eyagassab.lumina.data.remote.RetrofitClient;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import retrofit2.Response;

public class ConceptRepository {

    private static final String TAG = "ConceptRepository";

    private final ConceptDao conceptDao;
    private final LuminaApiService apiService;

    public ConceptRepository(Context context) {
        this.conceptDao = LuminaDatabase.getInstance(context).conceptDao();
        this.apiService = RetrofitClient.getApiService();
    }

    /** Source unique de vérité pour l'UI : lecture locale Room uniquement. */
    public LiveData<List<Concept>> observeConcepts() {
        return conceptDao.observeAllConcepts();
    }

    /**
     * Synchronisation bloquante (à appeler uniquement sur un thread d'arrière-plan ou un Worker).
     * Retourne true si les données ont été récupérées et enregistrées dans Room, false sinon.
     * Ne supprime jamais les données locales en cas d'erreur réseau.
     */
    public boolean syncDailyConceptsBlocking() {
        try {
            Response<DailyConceptsResponseDto> response = apiService.getDailyConcepts().execute();
            if (!response.isSuccessful() || response.body() == null || response.body().getConcepts() == null) {
                Log.w(TAG, "Échec HTTP lors de la synchronisation : code=" + response.code());
                return false;
            }

            List<Concept> entities = new ArrayList<>();
            for (ConceptDto dto : response.body().getConcepts()) {
                entities.add(new Concept(
                        dto.getId(),
                        dto.getTitle(),
                        dto.getTldr(),
                        dto.getPracticalApplication()
                ));
            }

            conceptDao.insertAll(entities);
            Log.i(TAG, "Synchronisation réussie : " + entities.size() + " concepts enregistrés dans Room.");
            return true;
        } catch (IOException e) {
            Log.e(TAG, "Erreur réseau lors de la synchronisation (les données locales sont préservées).", e);
            return false;
        }
    }
}