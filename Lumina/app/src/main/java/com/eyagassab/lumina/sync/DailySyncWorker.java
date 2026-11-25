package com.eyagassab.lumina.sync;

import android.content.Context;
import android.util.Log;

import androidx.annotation.NonNull;
import androidx.work.Worker;
import androidx.work.WorkerParameters;

import com.eyagassab.lumina.data.ConceptRepository;

public class DailySyncWorker extends Worker {

    private static final String TAG = "DailySyncWorker";

    public DailySyncWorker(@NonNull Context context, @NonNull WorkerParameters workerParams) {
        super(context, workerParams);
    }

    @NonNull
    @Override
    public Result doWork() {
        Log.i(TAG, "Démarrage de la synchronisation en arrière-plan (tentative #" + (getRunAttemptCount() + 1) + ")");

        ConceptRepository repository = new ConceptRepository(getApplicationContext());
        boolean success = repository.syncDailyConceptsBlocking();

        if (success) {
            Log.i(TAG, "DailySyncWorker terminé avec succès.");
            return Result.success();
        }

        // En cas d'erreur réseau, on demande un retry automatique (les données Room restent intactes)
        Log.w(TAG, "Échec de la synchronisation, nouvelle tentative planifiée (Result.retry).");
        return Result.retry();
    }
}