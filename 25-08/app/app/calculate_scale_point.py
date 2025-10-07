W_pixel = [136,132,133,134,139,141,143,147,154,163,171,178,183]
H_pixel = [146,149,152,156,161,162,164,166,173,177,180,185,188]

W_real = 3.9  # mm
H_real = 4.0  # mm

scale_w = [W_real / w for w in W_pixel]
scale_h = [H_real / h for h in H_pixel]
scale_avg = [(sw + sh)/2 for sw, sh in zip(scale_w, scale_h)]
print(scale_avg)
arr_scale_avg  = []
for i, (sw, sh, sa) in enumerate(zip(scale_w, scale_h, scale_avg)):
    print(f"Z={i}: scale_w={sw:.4f}, scale_h={sh:.4f}, scale_avg={sa:.4f} mm/pixel")
    arr_scale_avg.append(f"{sa:.8f}")
arr_int = [(float(x)) for x in arr_scale_avg]
print(arr_int)
