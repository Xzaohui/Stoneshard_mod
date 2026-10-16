# SQ08 分层避风棚附件交付记录

日期：2026-10-16。

冻结清单由绘图者确认，共 8 张。全部已保存到 Library，8 项均 succeeded，本地身份记录已成功写入。上传前后文件 SHA-256 一致。

父任务已发送全部 8 张附件，消息服务返回 accepted。消息 ID：`Sentinel_111e0a859c6c8191bfa2a97394f57de8`；时间：`2026-10-16T09:52:41.628172Z`。accepted 表示消息服务已接受，不等同于用户已查看。未重复发送。

## 附件顺序与对应关系

1. 真实盖顶：`previews/roof_on_actual.png`
   - Library 文件名：`roof_on_actual.png`
   - Library ID：`libfile_e31c492998b48191930b110fcd4a93fa`
   - 文件 ID：`file_00000000738481f6a248c58b2a7ea959`
   - 版本：0
   - SHA-256：`7fa087edfa0e1f412adca79dac202a145b00428e84267497df29d3342cfe53d1`
2. 揭顶 / 盖顶对照：`previews/roof_off_on_actual_comparison.png`
   - Library 文件名：`roof_off_on_actual_comparison(4).png`
   - Library ID：`libfile_b8fbaf3b0c088191a652dfd438c27eb8`
   - 文件 ID：`file_00000000760081f8b83468a9a0f5b6b9`
   - 版本：0
   - SHA-256：`25a6397199b14ec65e25cead9d9989e8e15bf0592853b74f6163a86ee3f65f25`
3. 独立地面：`layers/00_ground.png`
   - Library 文件名：`00_ground.png`
   - Library ID：`libfile_04b5e326f1888191bb27540a998af93a`
   - 文件 ID：`file_00000000d7dc8210b458518d8c8fa5de`
   - 版本：0
   - SHA-256：`cda38b08d7feff5a33e53071e938bf651cb0908df5620b6e821a927541906536`
4. 独立棚架：`layers/01_frame.png`
   - Library 文件名：`01_frame.png`
   - Library ID：`libfile_dba5c4dff12c8191bbeb23ad7b01dfe3`
   - 文件 ID：`file_00000000656c81fda2121b3095d483c1`
   - 版本：0
   - SHA-256：`af01d25008e328baef241e4a7a502b87e70a5e42bf99dc4060422cadf33e7934`
5. 独立屋顶：`layers/02_roof.png`
   - Library 文件名：`02_roof(1).png`
   - Library ID：`libfile_ce5aef05438c81919d3470f4f497cd6e`
   - 文件 ID：`file_00000000a15481f590bdf20b1183c2fe`
   - 版本：0
   - SHA-256：`d2e041fbaba551a758df5bc7e4a6b03a1e8d4b8ce9758d062307083e98256901`
6. 独立桌凳：`layers/03_furniture.png`
   - Library 文件名：`03_furniture.png`
   - Library ID：`libfile_9a8669ec3a308191b38363777a0e9a4a`
   - 文件 ID：`file_00000000661881fda2dc91f65e9704dc`
   - 版本：0
   - SHA-256：`17f8ae3d2e4aab2bfd4459c58025c719568d10840a8d1a19e8a87ac64d900b04`
7. 独立文书袋：`layers/04_document_pouch.png`
   - Library 文件名：`04_document_pouch.png`
   - Library ID：`libfile_e54002b882dc8191936b7f61e610352d`
   - 文件 ID：`file_00000000b24081f5bde1fdd69bad1879`
   - 版本：0
   - SHA-256：`8ee9f76410aa496869507ba62310eeb89db062f65e2919d04772bf5595c18552`
8. 独立前景：`layers/05_foreground.png`
   - Library 文件名：`05_foreground.png`
   - Library ID：`libfile_19847494a170819192d11759be16df39`
   - 文件 ID：`file_000000000d0c81fdafea2ed4e2865119`
   - 版本：0
   - SHA-256：`4c61cba31b81e51a6838139cca9036ae29439d7f8f9eaf5fc477818a8688f6b2`

## 说明

- 真实盖顶为 1536×1024，揭顶 / 盖顶对照为 3072×1024。
- 6 张独立图层均为 1536×1024 RGBA。
- 交付记录写入 delivery/，未改动图像、代码或游戏包，未提交或 push。
- 完整机器可读对应关系见 library_upload_results.json；冻结文件规格见 frozen_file_manifest.json。
