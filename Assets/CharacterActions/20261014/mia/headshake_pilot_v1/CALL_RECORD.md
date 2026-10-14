# Image generation call record
Five serial built-in image_gen__imagegen calls: K1_v1, K2_v1, K2_v2 (sole hard-error correction for reversed braid/hair), K3_v1, K3_v2 (sole hard-error correction for foot geometry). K1/K2/K3 v1 exact params were loaded with exec_command cat then JSON.parse and passed unmodified to the tool. K2_v2 appended a targeted correction to K2_v1 in memory, saved that object as params and text before passing the same object to the tool. The spec lock was reread before every call.

Full tool-return objects are in returns/, including complete image_url base64 payload and output_hint. Tool returns do not include server parameter echoes. PROVENANCE_VERIFICATION.json independently decodes payload and checks raw bytes and saved prompt/params equality; pre-call params are author-side records. K1 first shell-based return-save attempt hit OS argument-length limit, then the same stored return was saved with apply_patch; there was no extra generation.

No script drawing, body movement, compositing heads, deformation or interpolation. Boards use entire raw canvases with the same 1/2 nearest-neighbor scale. No per-frame fitting or aligning. Raw generated alpha retained. All failed candidates retained.

K3_v2 params were saved before the tool call; the identical object was passed to image_gen. Input 1 was K3_v1 edit target and input 2 approved mother body reference, both visually inspected beforehand. K3_v2 still failed strict foot registration and is not selected.
