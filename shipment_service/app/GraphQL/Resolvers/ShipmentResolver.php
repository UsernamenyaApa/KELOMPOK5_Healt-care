<?php

namespace App\GraphQL\Resolvers;

use App\Models\Shipment;
use App\Services\OrderServiceClient;
use App\Services\UserServiceClient;
use Carbon\Carbon;
use GraphQL\Type\Definition\ResolveInfo;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
use Nuwave\Lighthouse\Support\Contracts\GraphQLContext;

class ShipmentResolver
{
    protected OrderServiceClient $orderService;
    protected UserServiceClient $userService;

    public function __construct(OrderServiceClient $orderService, UserServiceClient $userService)
    {
        $this->orderService = $orderService;
        $this->userService = $userService;
    }

    // === RESOLVER UNTUK RELASI (NESTED QUERY) ===

    /**
     * Mengambil data order dari order_service.
     */
    public function order(Shipment $shipment, array $args, GraphQLContext $context, ResolveInfo $resolveInfo): ?array
    {
        Log::info("ShipmentResolver: Mengambil data order untuk order_id: {$shipment->order_id}");
        return $this->orderService->getOrder((string) $shipment->order_id);
    }

    /**
     * Mengambil data user dari user_service.
     */
    public function user(?array $order, array $args, GraphQLContext $context, ResolveInfo $resolveInfo): ?array
    {
        if (!$order || !isset($order['user_id'])) {
            return null;
        }
        Log::info("ShipmentResolver: Mengambil data user untuk user_id: {$order['user_id']}");
        return $this->userService->getUser((string) $order['user_id']);
    }

    // === RESOLVER UNTUK KUERI ===

    /**
     * Mengambil satu data pengiriman berdasarkan ID-nya.
     */
    public function byId(null $_, array $args, GraphQLContext $context, ResolveInfo $resolveInfo): ?Shipment
    {
        Log::info("ShipmentResolver: Mencari shipment dengan ID: {$args['id']}");
        return Shipment::find($args['id']);
    }

    /**
     * Mengambil data pengiriman berdasarkan ID Order.
     */
    public function byOrder(null $_, array $args, GraphQLContext $context, ResolveInfo $resolveInfo): Collection
    {
        Log::info("ShipmentResolver: Mencari shipment dengan order_id: {$args['order_id']}");
        return Shipment::where('order_id', $args['order_id'])->get();
    }

    /**
     * Mengambil semua pengiriman milik satu user.
     */
    public function byUser(null $_, array $args, GraphQLContext $context, ResolveInfo $resolveInfo): Collection
    {
        Log::info("ShipmentResolver: Mencari shipments untuk user_id: {$args['user_id']}");
        return Shipment::where('user_id', $args['user_id'])->get();
    }

    // === RESOLVER UNTUK MUTASI ===

    /**
     * Membuat pengiriman baru untuk sebuah order.
     */
    public function create(null $_, array $args, GraphQLContext $context, ResolveInfo $resolveInfo): Shipment
    {
        Log::info("ShipmentResolver: Mencoba membuat shipment untuk order_id: {$args['order_id']}");
        return DB::transaction(function () use ($args) {
            $order = $this->orderService->getOrder($args['order_id']);
            if (!$order || !in_array($order['status'], ['pending', 'processing'])) {
                throw new \Exception("Pengiriman tidak bisa dibuat untuk order dengan status '{$order['status']}'.");
            }

            if ((string) $args['user_id'] !== (string) $order['user_id']) {
                throw new \Exception('User ID yang diberikan tidak cocok dengan User ID pada order.');
            }

            $user = $this->userService->getUser($args['user_id']);
            if (!$user || empty($user['addresses'])) {
                throw new \Exception('Alamat pengiriman tidak ditemukan untuk user ini.');
            }
            $address = $user['addresses'][0];
            $shippingAddress = "{$address['street']}, {$address['city']}, {$address['zip_code']}";

            $shipment = Shipment::create([
                'order_id' => $args['order_id'],
                'user_id' => $args['user_id'],
                'tracking_number' => $args['tracking_number'] ?? 'TRK' . strtoupper(uniqid()),
                'carrier' => $args['carrier'] ?? 'Internal Courier',
                'status' => 'pending',
                'shipping_address' => $shippingAddress,
                'estimated_delivery' => Carbon::now()->addDays(3),
            ]);

            $shipment->updates()->create(['status' => 'pending', 'description' => 'Shipment has been created.']);
            $this->orderService->updateOrderStatus($args['order_id'], 'processing');

            return $shipment;
        });
    }

    /**
     * Memperbarui status sebuah pengiriman.
     */
    public function updateStatus(null $_, array $args, GraphQLContext $context, ResolveInfo $resolveInfo): ?Shipment
    {
        $shipment = Shipment::find($args['id']);
        if (!$shipment) { throw new \Exception('Shipment not found.'); }
        
        return DB::transaction(function () use ($args, $shipment) {
            $oldStatus = $shipment->status;
            $newStatus = $args['status'];

            $updateData = ['status' => $newStatus];
            if (isset($args['estimated_delivery'])) {
                $updateData['estimated_delivery'] = Carbon::parse($args['estimated_delivery']);
            }
            
            $shipment->update($updateData);

            $shipment->updates()->create([
                'status' => $newStatus,
                'location' => $args['location'] ?? 'N/A',
                'description' => $args['description'] ?? "Status updated from {$oldStatus} to {$newStatus}",
            ]);

            if (in_array($newStatus, ['delivered', 'cancelled', 'failed'])) {
                $this->orderService->updateOrderStatus($shipment->order_id, $newStatus);
            }

            return $shipment->fresh();
        });
    }

    /**
     * Menghapus data pengiriman.
     */
    public function deleteShipment(null $_, array $args, GraphQLContext $context, ResolveInfo $resolveInfo): ?Shipment
    {
        $shipment = Shipment::find($args['id']);
        if ($shipment) {
            $shipment->delete();
        }
        return $shipment;
    }
}