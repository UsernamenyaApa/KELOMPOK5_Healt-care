<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Shipment extends Model
{
    use HasFactory;

    protected $fillable = [
        'order_id',
        'user_id',
        'tracking_number',
        'carrier',
        'status',
        'shipping_address',
        'estimated_delivery',
    ];

    protected $casts = [
        'estimated_delivery' => 'datetime',
    ];

    public function updates(): HasMany
    {
        return $this->hasMany(ShipmentUpdate::class);
    }
    // Tidak ada relasi Eloquent untuk order() atau user() di sini
    // karena mereka di database yang berbeda, akan diambil via HTTP Client.
}