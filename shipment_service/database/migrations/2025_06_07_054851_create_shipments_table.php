<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('shipments', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('order_id')->unique(); // Setiap order hanya punya 1 shipment
            $table->unsignedBigInteger('user_id'); // Untuk memudahkan lookup shipment oleh user
            $table->string('tracking_number')->unique()->nullable();
            $table->string('carrier')->nullable(); // Misal: JNE, TIKI, Pos Indonesia
            $table->string('status')->default('pending'); // Enum: pending, in_transit, delivered, failed, cancelled
            $table->text('shipping_address'); // Alamat pengiriman lengkap (disimpan dari user_service)
            $table->timestamp('estimated_delivery')->nullable();
            $table->timestamps();

            // Catatan: order_id dan user_id tidak memiliki foreign key constraint langsung di sini.
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('shipments');
    }
};
