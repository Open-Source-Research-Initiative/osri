# Generate one MOVi-A research-dataset scene

[Greff et al. (CVPR 2022)](https://arxiv.org/abs/2203.03570) introduce Kubric and MOVi-A. Section 4.1 and Figure 5 describe 24-frame clips with up to 10 moving objects. We ran their paper-date worker on CPU to generate a new seeded scene with seven moving objects, editable Blender/Bullet states, rendered frames and annotations.

Use an isolated Python 3.9 environment. Install requirements.txt, run `python fetch-runtime.py`, then `python run.py` and `python compare.py`. The retrieval script pins author source9a868cc735de955709c4c75d9655fff1e90c72e4 and verifies the OCI digest/layers for the authors compiled Blender 2.93 module. No Docker daemon or privileged container is needed. Approximately 135 MB of compressed runtime layers are retrieved; Python dependencies and source code need additional space. The renderer is CPU-bound and the portable harness limits it to two available CPUs.

The source worker retains its CLEVR-style objects, background, camera, 12 fps, 256 × 256 resolution, 64 render samples per pixel, and 240 Hz physics. Seed 42 selects seven objects. Run output includes 24 RGBA frames, 24 instance-mask frames, depth, forward/backward flow, normals, object coordinates, camera/object metadata, collision events and native scene.blend/scene.bullet states.

The checked run passed frame-count, resolution, instance-count, label-range, finite-depth and object-motion checks. A second complete numerical/rendered scene was also generated while resolving an optional hypertune-reporting dependency; its earlier nonzero exit is retained. The comparison record states whether repeated object metadata and frame hashes match.

This reconstructs an author dataset-generation example and checks published design properties. It does not reconstruct the exact sampled Figure 5 scene or reproduce Table 3 SAVi/SIMONe foreground ARI. Exact 2022 asset bytes are not established, and modern PyBullet/TensorFlow packages differ from the original full Docker environment. Human scientific review is pending.

Keep ATTRIBUTION.md with imagery and native scenes: KuBasic geometry and derived imagery/native scenes are CC BY-SA 4.0. Kubric code is Apache-2.0; Blender has separate GPL terms. These terms are separate from the hub text license.

## Download the recorded files

- [comparison.json](files/blender/external/robotics/kubric-final-output/comparison.json) — generated render/annotation or comparison.
- [data_ranges.json](files/blender/external/robotics/kubric-final-output/data_ranges.json) — generated render/annotation or comparison.
- [events.json](files/blender/external/robotics/kubric-final-output/events.json) — generated render/annotation or comparison.
- [metadata.json](files/blender/external/robotics/kubric-final-output/metadata.json) — generated render/annotation or comparison.
- [preview.png](files/blender/external/robotics/kubric-final-output/preview.png) — generated render/annotation or comparison.
- [rgba_00000.png](files/blender/external/robotics/kubric-final-output/rgba_00000.png) — generated render/annotation or comparison.
- [rgba_00001.png](files/blender/external/robotics/kubric-final-output/rgba_00001.png) — generated render/annotation or comparison.
- [rgba_00002.png](files/blender/external/robotics/kubric-final-output/rgba_00002.png) — generated render/annotation or comparison.
- [rgba_00003.png](files/blender/external/robotics/kubric-final-output/rgba_00003.png) — generated render/annotation or comparison.
- [rgba_00004.png](files/blender/external/robotics/kubric-final-output/rgba_00004.png) — generated render/annotation or comparison.
- [rgba_00005.png](files/blender/external/robotics/kubric-final-output/rgba_00005.png) — generated render/annotation or comparison.
- [rgba_00006.png](files/blender/external/robotics/kubric-final-output/rgba_00006.png) — generated render/annotation or comparison.
- [rgba_00007.png](files/blender/external/robotics/kubric-final-output/rgba_00007.png) — generated render/annotation or comparison.
- [rgba_00008.png](files/blender/external/robotics/kubric-final-output/rgba_00008.png) — generated render/annotation or comparison.
- [rgba_00009.png](files/blender/external/robotics/kubric-final-output/rgba_00009.png) — generated render/annotation or comparison.
- [rgba_00010.png](files/blender/external/robotics/kubric-final-output/rgba_00010.png) — generated render/annotation or comparison.
- [rgba_00011.png](files/blender/external/robotics/kubric-final-output/rgba_00011.png) — generated render/annotation or comparison.
- [rgba_00012.png](files/blender/external/robotics/kubric-final-output/rgba_00012.png) — generated render/annotation or comparison.
- [rgba_00013.png](files/blender/external/robotics/kubric-final-output/rgba_00013.png) — generated render/annotation or comparison.
- [rgba_00014.png](files/blender/external/robotics/kubric-final-output/rgba_00014.png) — generated render/annotation or comparison.
- [rgba_00015.png](files/blender/external/robotics/kubric-final-output/rgba_00015.png) — generated render/annotation or comparison.
- [rgba_00016.png](files/blender/external/robotics/kubric-final-output/rgba_00016.png) — generated render/annotation or comparison.
- [rgba_00017.png](files/blender/external/robotics/kubric-final-output/rgba_00017.png) — generated render/annotation or comparison.
- [rgba_00018.png](files/blender/external/robotics/kubric-final-output/rgba_00018.png) — generated render/annotation or comparison.
- [rgba_00019.png](files/blender/external/robotics/kubric-final-output/rgba_00019.png) — generated render/annotation or comparison.
- [rgba_00020.png](files/blender/external/robotics/kubric-final-output/rgba_00020.png) — generated render/annotation or comparison.
- [rgba_00021.png](files/blender/external/robotics/kubric-final-output/rgba_00021.png) — generated render/annotation or comparison.
- [rgba_00022.png](files/blender/external/robotics/kubric-final-output/rgba_00022.png) — generated render/annotation or comparison.
- [rgba_00023.png](files/blender/external/robotics/kubric-final-output/rgba_00023.png) — generated render/annotation or comparison.
- [scene.blend](files/blender/external/robotics/kubric-final-output/scene.blend) — native model/state.
- [segmentation_00000.png](files/blender/external/robotics/kubric-final-output/segmentation_00000.png) — generated render/annotation or comparison.
- [segmentation_00001.png](files/blender/external/robotics/kubric-final-output/segmentation_00001.png) — generated render/annotation or comparison.
- [segmentation_00002.png](files/blender/external/robotics/kubric-final-output/segmentation_00002.png) — generated render/annotation or comparison.
- [segmentation_00003.png](files/blender/external/robotics/kubric-final-output/segmentation_00003.png) — generated render/annotation or comparison.
- [segmentation_00004.png](files/blender/external/robotics/kubric-final-output/segmentation_00004.png) — generated render/annotation or comparison.
- [segmentation_00005.png](files/blender/external/robotics/kubric-final-output/segmentation_00005.png) — generated render/annotation or comparison.
- [segmentation_00006.png](files/blender/external/robotics/kubric-final-output/segmentation_00006.png) — generated render/annotation or comparison.
- [segmentation_00007.png](files/blender/external/robotics/kubric-final-output/segmentation_00007.png) — generated render/annotation or comparison.
- [segmentation_00008.png](files/blender/external/robotics/kubric-final-output/segmentation_00008.png) — generated render/annotation or comparison.
- [segmentation_00009.png](files/blender/external/robotics/kubric-final-output/segmentation_00009.png) — generated render/annotation or comparison.
- [segmentation_00010.png](files/blender/external/robotics/kubric-final-output/segmentation_00010.png) — generated render/annotation or comparison.
- [segmentation_00011.png](files/blender/external/robotics/kubric-final-output/segmentation_00011.png) — generated render/annotation or comparison.
- [segmentation_00012.png](files/blender/external/robotics/kubric-final-output/segmentation_00012.png) — generated render/annotation or comparison.
- [segmentation_00013.png](files/blender/external/robotics/kubric-final-output/segmentation_00013.png) — generated render/annotation or comparison.
- [segmentation_00014.png](files/blender/external/robotics/kubric-final-output/segmentation_00014.png) — generated render/annotation or comparison.
- [segmentation_00015.png](files/blender/external/robotics/kubric-final-output/segmentation_00015.png) — generated render/annotation or comparison.
- [segmentation_00016.png](files/blender/external/robotics/kubric-final-output/segmentation_00016.png) — generated render/annotation or comparison.
- [segmentation_00017.png](files/blender/external/robotics/kubric-final-output/segmentation_00017.png) — generated render/annotation or comparison.
- [segmentation_00018.png](files/blender/external/robotics/kubric-final-output/segmentation_00018.png) — generated render/annotation or comparison.
- [segmentation_00019.png](files/blender/external/robotics/kubric-final-output/segmentation_00019.png) — generated render/annotation or comparison.
- [segmentation_00020.png](files/blender/external/robotics/kubric-final-output/segmentation_00020.png) — generated render/annotation or comparison.
- [segmentation_00021.png](files/blender/external/robotics/kubric-final-output/segmentation_00021.png) — generated render/annotation or comparison.
- [segmentation_00022.png](files/blender/external/robotics/kubric-final-output/segmentation_00022.png) — generated render/annotation or comparison.
- [segmentation_00023.png](files/blender/external/robotics/kubric-final-output/segmentation_00023.png) — generated render/annotation or comparison.
- [fetch-runtime.py](files/blender/fetch-runtime.py) — portable driver or environment/source record.
- [run.py](files/blender/run.py) — portable driver or environment/source record.
- [compare.py](files/blender/compare.py) — portable driver or environment/source record.
- [requirements.txt](files/blender/requirements.txt) — portable driver or environment/source record.
- [requirements-tested.txt](files/blender/requirements-tested.txt) — portable driver or environment/source record.
- [ATTRIBUTION.md](files/blender/ATTRIBUTION.md) — portable driver or environment/source record.

[Complete run record](records/blender.json) · [All candidate attempts](README.md). Human scientific review is pending.
