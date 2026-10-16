using System.Globalization;
using System.IO;
using System.Text.Json;
using System.Text.RegularExpressions;
using UndertaleModLib;
using UndertaleModLib.Decompiler;

// Executes only EAO's compiled callback instructions. Native inventory/GUI calls
// are deterministic test doubles, so this is NOT a GameMaker runtime/UI test.
internal static class EaoActionChecks
{
    public static string[] Validate(UndertaleData data)
    {
        var night=data.GameObjects.Any(o=>o.Name.Content=="o_eao_n1_mara");
        var roots=new List<string>{"gml_Object_o_eao_courier_Create_0","gml_Object_o_eao_d01_clerk_Create_0"};
        if(night) roots.Add("gml_Object_o_eao_n1_mara_Create_0");
        var assembly = string.Join("\n", roots.Select(name => {
            var parent = data.Code.Single(c => c.Name.Content == name);
            return parent.Disassemble(data.Variables, data.CodeLocals.For(parent));
        }));
        var methods = new Dictionary<string, string>();
        foreach (Match match in Regex.Matches(assembly, @"push\.i (?<code>gml_Script_anon_\S+)\s+conv\.i\.v\s+pushi\.e -1\s+conv\.i\.v\s+call\.i method\(argc=2\)\s+pop\.v\.v self\.(?<method>eao_\w+)")) {
            var start = assembly.IndexOf("> " + match.Groups["code"].Value + " ", StringComparison.Ordinal);
            var end = assembly.IndexOf("\n> ", start + 2, StringComparison.Ordinal);
            methods.Add(match.Groups["method"].Value, end < 0 ? assembly[start..] : assembly[start..end]);
        }
        if (methods.Count != (night?22:9)) throw new InvalidDataException("Compiled callback assignments could not be resolved.");
        foreach(var pair in new[]{("test_toggle","gml_Object_o_eao_controller_KeyPress_119"),("test_click","gml_Object_o_globalmapInteractiveNormal_Other_20"),("test_execute","gml_Object_o_eao_controller_Other_13"),("test_commit","gml_Object_o_smoothRoomChanger_Other_20"),("test_arrival","gml_Object_o_eao_controller_Step_2"),("test_annex_spawn","gml_Object_o_eao_controller_Other_14"),("test_annex_gate","gml_Object_o_eao_d01_entry_Step_0")}) {
            var code=data.Code.Single(c=>c.Name.Content==pair.Item2);
            methods[pair.Item1]=code.Disassemble(data.Variables,data.CodeLocals.For(code));
        }
        var eastSurface = data.Rooms.Any(r => r.Name.Content == "r_eao_n2_world");
        var devWarp = data.Code.SingleOrDefault(c=>c.Name.Content=="gml_Object_o_eao_devtools_Other_11");
        if(devWarp!=null) methods["test_dev_warp"]=devWarp.Disassemble(data.Variables,data.CodeLocals.For(devWarp));
        if (eastSurface) foreach (var pair in new[] { ("test_geo_return", "gml_Object_o_eao_n2_home_Step_0"), ("test_geo_enter", "gml_Object_o_eao_site_door_shed_Alarm_7") }) {
            var code = data.Code.Single(c => c.Name.Content == pair.Item2);
            methods[pair.Item1] = code.Disassemble(data.Variables, data.CodeLocals.For(code));
        }
        var objects = new[] { "letter", "enclosure", "receipt", "copy", "permit", "manifest", "packing", "seal" }.Select(id => data.GameObjects.IndexOf(data.GameObjects.Single(o => o.Name.Content == "o_inv_eao_" + id))).ToArray();
        int inventoryObject = data.GameObjects.IndexOf(data.GameObjects.Single(o => o.Name.Content == "o_inventory"));
        var passed = new List<string>();
        void Test(string name, Action<Vm> action) {
            var vm = new Vm(methods, objects, inventoryObject, data);
            action(vm); passed.Add(name);
        }
        static void Require(bool condition, string message) { if (!condition) throw new InvalidDataException("Compiled EAO action regression: " + message); }
        if (eastSurface) {
            foreach (var source in new[] { "missing", "r_eao_n2_sites", "r_eao_n2_world", "r_taverninside1floor" })
                Test("east-building-return-persisted-source-" + source, vm => {
                    if (source != "missing") vm.Map["EAO_geo_sites_return"] = source;
                    vm.Run("test_geo_return");
                    Require(vm.DoorTarget == vm.RoomIndex(source == "r_eao_n2_world" ? "r_eao_n2_world" : "r_eao_n2_sites") &&
                        vm.PositionTag == "NA" && vm.GridX == 29 && vm.GridY == 15 && vm.Items.Count == 0, "geographical return must keep native marker/world coordinates and safe legacy fallback");
                });
            foreach (var source in new[] { "r_eao_n2_sites", "r_eao_n2_world" })
                Test("east-building-enter-records-native-source-" + source, vm => {
                    vm.CurrentRoom = vm.RoomIndex(source); vm.NativeDoorCreatesChanger = true;
                    vm.Run("test_geo_enter");
                    Require((string)vm.Map["EAO_geo_sites_return"]! == source && vm.Changer && vm.Map.Count == 1, "successful native door origin");
                });
            Test("east-building-failed-or-pending-door-keeps-origin", vm => {
                vm.Map["EAO_geo_sites_return"] = "r_eao_n2_sites"; vm.CurrentRoom = vm.RoomIndex("r_eao_n2_world");
                vm.Run("test_geo_enter"); Require((string)vm.Map["EAO_geo_sites_return"]! == "r_eao_n2_sites", "failed native door overwrote origin");
                vm.Changer = true; vm.Run("test_geo_enter"); Require((string)vm.Map["EAO_geo_sites_return"]! == "r_eao_n2_sites", "pending changer overwrote origin");
            });
        }
        Test("accept-places-three-documents-before-state", vm => {
            Require(vm.Run("eao_accept") == 0 && vm.State == 1 && vm.Carried == 3, "accept");
            Require(vm.Run("eao_resume") == 1 && vm.Run("eao_register_verren") == 1 && vm.State == 1, "unread gate");
        });
        Test("full-inventory-rolls-back-partial-handover", vm => {
            vm.Capacity = 2;
            Require(vm.Run("eao_accept") == 1 && vm.Items.Count == 0 && vm.State == 0, "atomic initial placement");
        });
        Test("native-create-failure-rolls-back", vm => {
            vm.FailCreation = 2;
            Require(vm.Run("eao_accept") == 1 && vm.Items.Count == 0 && vm.State == 0, "native creation failure");
        });
        Test("partial-reading-does-not-complete", vm => {
            vm.Run("eao_accept"); vm.Map["EAO_read_eao_letter"] = 1;
            Require(vm.Run("eao_resume") == 1 && vm.Run("eao_register_copy") == 1 && vm.State == 1, "partial reading");
        });
        foreach (var choice in new[] { "verren", "copy" }) Test("read-carry-complete-" + choice + "-once", vm => {
            vm.Run("eao_accept"); vm.ReadOriginals();
            Require(vm.Run("eao_resume") == 2 && vm.Run("eao_register_" + choice) == 0 && vm.State == 2 && vm.Carried == 4, "completion");
            Require((string)vm.Map["EAO_MQ01_choice"]! == (choice == "verren" ? "verren" : "copy_first"), "chosen branch");
            vm.Run("eao_register_" + choice); vm.Run("eao_recover");
            Require(vm.Items.Count == 4 && vm.State == 2, "duplicate reward");
        });
        Test("copy-must-fit-before-completion", vm => {
            vm.Run("eao_accept"); vm.ReadOriginals(); vm.Capacity = 3;
            Require(vm.Run("eao_register_verren") == 3 && vm.State == 1 && vm.Items.Count == 3 && !vm.Map.ContainsKey("EAO_E01"), "copy placement gate");
        });
        Test("read-flags-do-not-replace-carried-originals", vm => {
            vm.Run("eao_accept"); vm.ReadOriginals(); vm.Items.Remove(vm.Items.Keys.First());
            Require(vm.Run("eao_register_copy") == 2 && vm.State == 1 && vm.Items.Count == 2, "missing original");
        });
        Test("stash-does-not-count-as-carried-or-duplicate-on-recovery", vm => {
            vm.Run("eao_accept"); vm.ReadOriginals();
            foreach (var paper in vm.Items.Values) paper.Carried = false;
            Require(vm.Run("eao_register_verren") == 2 && vm.Run("eao_recover") == 0 && vm.Items.Count == 3 && vm.State == 1, "stash scope");
        });
        Test("legacy-accepted-progress-collects-papers", vm => {
            vm.Map["EAO_MQ01"] = 1;
            Require(vm.Run("eao_recover") == 0 && vm.State == 1 && vm.Carried == 3, "legacy accepted");
        });
        Test("legacy-completed-progress-collects-copy-without-reset", vm => {
            vm.Map["EAO_MQ01"] = 2; vm.Map["EAO_MQ01_choice"] = "verren";
            Require(vm.Run("eao_recover") == 0 && vm.State == 2 && vm.Carried == 4 && vm.Run("eao_resume") == 3, "legacy completed");
            Require(!vm.Map.ContainsKey("EAO_read_eao_copy") && (string)vm.Map["EAO_MQ01_choice"]! == "verren", "no fabricated read/choice");
        });
        void Ready(Vm vm) { vm.Capacity=8; vm.Run("eao_accept"); vm.ReadOriginals(); vm.Run("eao_register_verren"); vm.Map["EAO_read_eao_copy"]=1; }
        Test("mq02-refuses-without-read-carried-comparison", vm => {
            Require(vm.Run("eao_mq02_accept") == 2 && !vm.Map.ContainsKey("EAO_MQ02"), "MQ02 prerequisite");
            Ready(vm); vm.Items.Values.Single(p => p.Resource == objects[3]).Carried=false;
            Require(vm.Run("eao_mq02_accept") == 2, "MQ02 carried copy");
        });
        Test("mq02-permit-must-fit-before-acceptance", vm => {
            Ready(vm); vm.Capacity=4;
            Require(vm.Run("eao_mq02_accept") == 1 && !vm.Map.ContainsKey("EAO_MQ02") && vm.Items.Count == 4, "permit rollback");
        });
        Test("mq02-no-archive-copies-before-visit", vm => {
            Ready(vm); Require(vm.Run("eao_mq02_accept") == 0 && vm.Carried == 5, "permit acceptance");
            vm.Run("eao_mq02_recover");
            Require(vm.Carried == 5 && vm.Run("eao_mq02_submit") == 1, "archive visit gate");
        });
        Test("mq02-archive-copy-transaction-full-rollback", vm => {
            Ready(vm); vm.Run("eao_mq02_accept"); vm.Map["EAO_D01_archive_visited"]=1; vm.Capacity=7;
            Require(vm.Run("eao_mq02_recover") == 1 && vm.Items.Count == 5, "three archive papers rollback");
        });
        Test("mq02-read-visit-and-carry-required", vm => {
            Ready(vm); vm.Run("eao_mq02_accept"); vm.Map["EAO_D01_archive_visited"]=1; vm.Run("eao_mq02_recover");
            Require(vm.Carried == 8 && vm.Run("eao_mq02_submit") == 1, "unread archive papers");
            foreach (var id in new[] { "manifest", "packing", "seal" }) vm.Map["EAO_read_eao_"+id]=1;
            vm.Items.Values.Single(p => p.Resource == objects[5]).Carried=false;
            Require(vm.Run("eao_mq02_submit") == 2, "archive papers stash gate");
            vm.Items.Values.Single(p => p.Resource == objects[5]).Carried=true;
            vm.Map.Remove("EAO_D01_archive_visited"); Require(vm.Run("eao_mq02_submit") == 1, "fabricated read flag cannot replace visit");
        });
        Test("mq02-completes-once-preserves-original-choice-and-unverified-evidence", vm => {
            Ready(vm); vm.Run("eao_mq02_accept"); vm.Map["EAO_D01_archive_visited"]=1; vm.Run("eao_mq02_recover");
            foreach (var id in new[] { "manifest", "packing", "seal" }) vm.Map["EAO_read_eao_"+id]=1;
            Require(vm.Run("eao_mq02_submit") == 0 && (string)vm.Map["EAO_register_lead"]! == "old_canal" && NumberValue(vm.Map["EAO_MQ02"]) == 2, "MQ02 completion");
            vm.Run("eao_mq02_submit"); vm.Run("eao_mq02_recover");
            Require(vm.Carried == 8 && (string)vm.Map["EAO_E01"]! == "copied" && (string)vm.Map["EAO_MQ01_choice"]! == "verren", "MQ02 replay or evidence overclaim");
        });
        Test("map-f8-default-off-enable-disable-and-no-quest-reward-write", vm=> {
            vm.Run("test_click"); Require(vm.NativeFallbacks==1&&!vm.Map.ContainsKey("EAO_test_map_pending"),"default off");
            vm.Run("test_toggle"); Require(NumberValue(vm.Map["EAO_test_teleport_enabled"])==1,"F8 enable");
            vm.Run("test_toggle"); Require(NumberValue(vm.Map["EAO_test_teleport_enabled"])==0&&vm.Items.Count==0&&vm.Map.Keys.All(k=>k.StartsWith("EAO_test_")),"F8 disable/rewards");
        });
        Test("map-f8-disable-cancels-pending-click", vm=> {
            vm.Run("test_toggle"); vm.Run("test_click"); vm.Run("test_toggle"); vm.Run("test_execute");
            Require(!vm.Changer&&NumberValue(vm.Map["EAO_test_map_pending"])==0&&vm.GridX==29&&vm.GridY==15,"cancel pending click");
        });
        Test("map-f8-does-not-interrupt-native-transition", vm=> {
            vm.Changer=true; vm.Run("test_toggle"); Require(vm.Map.Count==0,"in-flight toggle");
        });
        Test("map-right-middle-wheel-and-hover-use-original-handler", vm=> {
            vm.Run("test_toggle"); foreach(var state in new[]{5,14,17,18,37,0,1}) {vm.GuiState=state;vm.Run("test_click");}
            Require(vm.NativeFallbacks==7&&NumberValue(vm.Map["EAO_test_map_pending"])==0,"native map actions");
        });
        Test("map-left-click-resolves-pan-and-half-full-zoom-without-hover-staleness", vm=> {
            vm.Run("test_toggle"); vm.Run("test_click");
            Require(NumberValue(vm.Map["EAO_test_map_x"])==26&&NumberValue(vm.Map["EAO_test_map_y"])==13,"half-scale coordinate");
            vm.MapScale=1;vm.Run("test_click"); Require(NumberValue(vm.Map["EAO_test_map_x"])==13&&NumberValue(vm.Map["EAO_test_map_y"])==6,"full-scale coordinate");
            vm.Drag=true;vm.Map["EAO_test_map_pending"]=0;vm.Run("test_click");Require(NumberValue(vm.Map["EAO_test_map_pending"])==0,"drag click");
        });
        Test("map-border-and-missing-room-refuse-without-world-writes",vm=> {
            vm.Run("test_toggle");vm.Border=true;vm.Run("test_click");Require(NumberValue(vm.Map["EAO_test_map_pending"])==0,"border");
            vm.Border=false;vm.MissingRoom=true;vm.Run("test_click");Require(NumberValue(vm.Map["EAO_test_map_pending"])==0&&vm.GridX==29&&vm.GridY==15,"missing room");
        });
        Test("map-combat-dungeon-and-turn-lock-keep-transition-safe",vm=> {
            vm.Run("test_toggle");vm.Run("test_click");vm.Combat=true;vm.Run("test_execute");Require(!vm.Changer&&NumberValue(vm.Map["EAO_test_map_pending"])==0,"combat");
            vm.Combat=false;vm.Run("test_click");vm.Dungeon=true;vm.Run("test_execute");Require(!vm.Changer&&NumberValue(vm.Map["EAO_test_map_pending"])==0,"dungeon");
            vm.Dungeon=false;vm.Run("test_click");vm.Locked=true;vm.Run("test_execute");Require(!vm.Changer&&NumberValue(vm.Map["EAO_test_map_pending"])==1,"turn lock");
        });
        if(devWarp!=null) {
            Test("dev-warp-default-off-cancel-and-malformed-coordinate-noop",vm=> {
                vm.DialogText="41,37";vm.Run("test_dev_warp");Require(!vm.Map.ContainsKey("EAO_test_map_pending"),"developer opt-in");
                vm.Dev=true;
                foreach(var text in new[]{"","abc","-1,3","1.2,3","1,2,3","1,","1","999,37","41,99"}) {
                    vm.DialogText=text;vm.Run("test_dev_warp");Require(!vm.Map.ContainsKey("EAO_test_map_pending"),"invalid input: "+text);
                }
            });
            Test("dev-warp-coordinate-combat-escape-preserves-source-until-saver",vm=> {
                vm.Dev=true;vm.Combat=true;vm.DialogText=" 41, 37 ";vm.Run("test_dev_warp");
                Require(NumberValue(vm.Map["EAO_test_map_x"])==41&&NumberValue(vm.Map["EAO_test_map_y"])==37,"coordinate parse");
                vm.Run("test_execute");Require(vm.Changer&&vm.Combat&&vm.GridX==29&&vm.GridY==15,"combat flags/source untouched");
                vm.Run("test_commit");Require(vm.GridX==41&&vm.GridY==37&&vm.Items.Count==0&&vm.State==0,"native commit/no reward");
                Require((string)vm.Map["EAO_dev_warp_origin_room"]! == "r_taverninside1floor"&&NumberValue(vm.Map["EAO_dev_warp_origin_x"])==325,"first origin");
            });
            Test("dev-warp-failed-transition-does-not-record-origin",vm=> {
                vm.Dev=true;vm.DialogText="41,37";vm.FailTransition=true;vm.Run("test_dev_warp");vm.Run("test_execute");
                Require(!vm.Changer&&!vm.Map.ContainsKey("EAO_dev_warp_origin_room")&&vm.GridX==29,"failed start");
            });
            Test("dev-warp-shift-return-preserves-first-room-world-and-local-position",vm=> {
                vm.Dev=true;vm.DialogText="41,37";vm.Run("test_dev_warp");vm.Run("test_execute");vm.Run("test_commit");
                vm.Changer=false;vm.CurrentRoom=vm.RequestedRoom;vm.DialogText="45,36";vm.Run("test_dev_warp");vm.Run("test_execute");vm.Run("test_commit");
                Require(NumberValue(vm.Map["EAO_dev_warp_origin_grid_x"])==29,"second hop overwrote origin");
                vm.Changer=false;vm.Shift=true;vm.Run("test_dev_warp");vm.Run("test_execute");
                Require(vm.RequestedRoom==vm.RoomIndex("r_taverninside1floor")&&vm.GridX==45,"return exact room/deferred coordinate");
                vm.Run("test_commit");Require(vm.GridX==29&&vm.GridY==15&&NumberValue(vm.Map["localX"])==325&&NumberValue(vm.Map["localY"])==454&&NumberValue(vm.Map["EAO_test_map_arrival"])==0,"return exact original position");
            });
            Test("dev-warp-no-origin-lock-dungeon-and-disabled-return-gates",vm=> {
                vm.Dev=true;vm.Shift=true;vm.Run("test_dev_warp");Require(vm.Map.Count==0,"no return origin");
                vm.Shift=false;vm.DialogText="41,37";vm.Locked=true;vm.Run("test_dev_warp");Require(vm.Map.Count==0,"action locked");
                vm.Locked=false;vm.Dungeon=true;vm.Run("test_dev_warp");Require(vm.Map.Count==0,"dungeon");
                vm.Dungeon=false;vm.Run("test_dev_warp");vm.Map["EAO_test_map_home"]=1;vm.Dev=false;vm.Run("test_execute");Require(!vm.Changer,"disabled developer return");
            });
        }
        Test("map-native-saver-before-coordinate-commit-and-failure-keeps-source",vm=> {
            vm.Run("test_toggle");vm.Run("test_click");vm.FailTransition=true;vm.Run("test_execute");
            Require(!vm.Changer&&!vm.Map.ContainsKey("EAO_test_map_commit")&&vm.GridX==29&&vm.GridY==15,"native creation failure");
            vm.FailTransition=false;vm.Run("test_click");vm.Run("test_execute");
            Require(vm.Changer&&vm.GridX==29&&vm.GridY==15&&NumberValue(vm.Map["EAO_test_map_commit"])==1,"source coordinates changed before saver");
            vm.Run("test_commit");Require(vm.GridX==26&&vm.GridY==13&&vm.PositionTag=="NA"&&vm.Map["localX"]==null&&vm.Map["localY"]==null&&NumberValue(vm.Map["EAO_test_map_arrival"])==1&&NumberValue(vm.Map["EAO_test_map_commit"])==0&&vm.State==0&&vm.Items.Count==0,"deferred native arrival/no rewards");
            vm.Run("test_commit");Require(vm.GridX==26&&vm.GridY==13,"commit replay");
        });
        void ArrivalReady(Vm vm) {
            vm.Run("test_toggle"); vm.Run("test_click"); vm.Run("test_execute"); vm.Run("test_commit");
            vm.Changer=false; vm.PlayerExists=false; vm.CurrentRoom=vm.RequestedRoom;
        }
        Test("map-arrival-waits-for-generated-abstract-player",vm=> {
            ArrivalReady(vm); vm.Run("test_arrival"); Require(vm.SpawnX==-50&&NumberValue(vm.Map["EAO_test_map_arrival"])==1,"generation wait");
            vm.AbstractExists=true; vm.Run("test_arrival"); Require(vm.SpawnX==156&&vm.SpawnY==156&&NumberValue(vm.Map["EAO_test_map_arrival"])==0,$"native placeholder arrival: {vm.SpawnX},{vm.SpawnY}, pending={vm.Map["EAO_test_map_arrival"]}");
        });
        Test("map-arrival-rejects-wall-isolated-marked-and-collision-tiles",vm=> {
            ArrivalReady(vm); vm.AbstractExists=true; vm.LandingObstacles=true; vm.Run("test_arrival");
            Require(vm.SpawnX==208&&vm.SpawnY==156,"walkable neighbour / collision / hazard filtering");
        });
        Test("map-arrival-rejects-swimming-even-when-native-astar-is-open",vm=> {
            ArrivalReady(vm);vm.AbstractExists=true;vm.WaterLanding=true;vm.Run("test_arrival");
            Require(vm.SpawnX==182&&vm.SpawnY==156,"dry landing and dry neighbour");
        });
        foreach(var fast in new[]{false,true}) Test("map-arrival-waits-for-native-water-markers-"+(fast?"rewind":"abstract"),vm=> {
            ArrivalReady(vm);vm.AbstractExists=!fast;vm.FastExists=fast;vm.WaterPending=true;
            vm.Run("test_arrival");
            Require(vm.SpawnX==-50&&vm.PlaceholderDelays==2&&!vm.Changer&&NumberValue(vm.Map["EAO_test_map_arrival"])==1,"water marker must finish before landing/spawn");
            vm.WaterPending=false;vm.WaterLanding=true;vm.Run("test_arrival");
            Require(vm.SpawnX==182&&vm.SpawnY==156&&NumberValue(vm.Map["EAO_test_map_arrival"])==0,"landing after native water grid initialization");
        });
        Test("map-all-water-target-returns-without-spawning-a-swimmer",vm=> {
            ArrivalReady(vm);vm.AbstractExists=true;vm.AllWater=true;vm.Run("test_arrival");
            Require(vm.Changer&&NumberValue(vm.Map["EAO_test_map_restore"])==1&&vm.SpawnX==-50,"all-water fallback");
        });
        Test("map-arrival-fast-rewind-placeholder-and-no-live-player-relocation",vm=> {
            ArrivalReady(vm); vm.FastExists=true; vm.PlayerExists=true; vm.Run("test_arrival");Require(vm.SpawnX==-50,"live player untouched");
            vm.PlayerExists=false; vm.Run("test_arrival"); Require(vm.SpawnX==156&&NumberValue(vm.Map["EAO_test_map_arrival"])==0,"native rewind placeholder arrival");
        });
        Test("map-unwalkable-target-returns-to-saved-source-through-native-changer",vm=> {
            ArrivalReady(vm); vm.AbstractExists=true; vm.NoLanding=true; vm.Run("test_arrival");
            Require(vm.Changer&&NumberValue(vm.Map["EAO_test_map_restore"])==1&&vm.SpawnX==-50,"unwalkable tile restoration scheduled");
            vm.Run("test_commit");Require(vm.GridX==29&&vm.GridY==15&&NumberValue(vm.Map["localX"])==325&&NumberValue(vm.Map["localY"])==454&&NumberValue(vm.Map["EAO_test_map_arrival"])==0,"source position restored");
        });
        Test("map-current-world-tile-can-reload-for-stranded-character-recovery",vm=> {
            vm.GridX=26;vm.GridY=13;vm.CurrentRoom=vm.RoomIndex("r_DockStore1floor");vm.Run("test_toggle");vm.Run("test_click");vm.Run("test_execute");Require(vm.Changer,"same-tile recovery reload");
        });
        Test("customs-entrance-visible-before-quest-and-spawned-once",vm=> {
            vm.CurrentRoom=vm.RoomIndex("r_DockStore1floor");vm.Run("test_annex_spawn");vm.Run("test_annex_spawn");
            Require(vm.EntryExists&&vm.EntryCreations==1&&vm.State==0&&vm.Items.Count==0,"physical entrance / duplicate / task state");
        });
        Test("customs-entrance-does-not-spawn-in-other-room-or-transition",vm=> {
            vm.Run("test_annex_spawn");Require(!vm.EntryExists,"wrong room");
            vm.CurrentRoom=vm.RoomIndex("r_DockStore1floor");vm.Changer=true;vm.Run("test_annex_spawn");Require(!vm.EntryExists,"in-flight transition");
            vm.Changer=false;vm.PlayerExists=false;vm.Run("test_annex_spawn");Require(!vm.EntryExists,"no native player yet");
        });
        Test("customs-entrance-native-lock-requires-completed-and-read-copy",vm=> {
            vm.Run("test_annex_gate");Require(vm.EntryLocked,"no paperwork");
            vm.Map["EAO_MQ01"]=2;vm.Run("test_annex_gate");Require(vm.EntryLocked,"unread copy");
            vm.Map["EAO_read_eao_copy"]=1;vm.Map["EAO_MQ01"]=1;vm.Run("test_annex_gate");Require(vm.EntryLocked,"unfinished quest");
            vm.Map["EAO_MQ01"]=2;vm.Run("test_annex_gate");Require(!vm.EntryLocked&&vm.EntryDepth==-1100&&vm.EntryName=="封账仓入口"&&vm.Items.Count==0,"eligible visible native doorway");
        });
        if(night) {
            void ReadyNight(Vm vm) {
                vm.Run("eao_n1_accept"); vm.CurrentRoom=vm.RoomIndex("r_eao_n1_yard");vm.Run("eao_n1_rope");
                vm.CurrentRoom=vm.RoomIndex("r_eao_n1_bellhouse");vm.Run("eao_n1_cots");vm.Run("eao_n1_reveal");
            }
            Test("night-independent-of-retired-quest-and-repeated-accept",vm=> {
                vm.Map["EAO_MQ01"]=1;vm.Map["EAO_read_eao_letter"]=1;
                Require(vm.Run("eao_n1_mara_resume")==0&&vm.Run("eao_n1_accept")==0,"new entry");
                vm.Run("eao_n1_accept");Require(NumberValue(vm.Map["EAO_N1_stage"])==1&&vm.State==1&&vm.Items.Count==0,"no legacy conversion or duplicate handover");
            });
            Test("night-scene-evidence-requires-actual-room",vm=> {
                vm.Run("eao_n1_accept");Require(vm.Run("eao_n1_rope")==1&&!vm.Map.ContainsKey("EAO_N1_rope"),"remote clue");
                vm.CurrentRoom=vm.RoomIndex("r_eao_n1_yard");vm.Run("eao_n1_rope");Require(vm.Run("eao_n1_cots")==1,"remote bedding");
            });
            Test("night-two-clues-required-before-confession",vm=> {
                vm.Run("eao_n1_accept");vm.CurrentRoom=vm.RoomIndex("r_eao_n1_bellhouse");
                Require(vm.Run("eao_n1_reveal")==1&&vm.Run("eao_n1_plan_shelter")==1,"premature truth or plan");
                vm.Run("eao_n1_cots");Require(vm.Run("eao_n1_reveal")==1,"one clue cannot force truth");
                vm.CurrentRoom=vm.RoomIndex("r_eao_n1_yard");vm.Run("eao_n1_rope");
                vm.CurrentRoom=vm.RoomIndex("r_eao_n1_bellhouse");Require(vm.Run("eao_n1_ivo_resume")==1&&NumberValue(vm.Map["EAO_N1_stage"])==1,"preview advanced truth");
                Require(vm.Run("eao_n1_reveal")==0&&NumberValue(vm.Map["EAO_N1_stage"])==2,"confession");
            });
            Test("night-plan-can-change-before-execution",vm=> {
                ReadyNight(vm);vm.Run("eao_n1_plan_shelter");vm.Run("eao_n1_plan_audit");
                Require((string)vm.Map["EAO_N1_plan"]! == "audit"&&NumberValue(vm.Map["EAO_N1_stage"])==3,"plan switch");
                vm.Run("eao_n1_plan_shelter");Require(!vm.Map.ContainsKey("EAO_N1_families"),"planning executed departure");
            });
            Test("night-shelter-requires-drain-and-correct-plan",vm=> {
                ReadyNight(vm);vm.Run("eao_n1_plan_shelter");Require(vm.Run("eao_n1_escort")==1,"off-scene departure");
                vm.Run("eao_n1_plan_audit");vm.CurrentRoom=vm.RoomIndex("r_eao_n1_underpass");Require(vm.Run("eao_n1_escort")==1,"wrong-route departure");
            });
            Test("night-shelter-outcome-and-idempotent-epilogue",vm=> {
                ReadyNight(vm);vm.Run("eao_n1_plan_shelter");vm.CurrentRoom=vm.RoomIndex("r_eao_n1_underpass");vm.Run("eao_n1_escort");
                Require((string)vm.Map["EAO_N1_families"]! == "hidden"&&(string)vm.Map["EAO_N1_ivo"]! == "escaped","shelter consequences");
                Require(vm.Run("eao_n1_plan_audit")==1,"final choice rewritable");
                vm.Run("eao_n1_tor_commit");Require((string)vm.Map["EAO_N1_families"]! == "hidden","opposite-route overwrite");
                Require(vm.Run("eao_n1_close")==0&&vm.Run("eao_n1_mara_resume")==3,"shelter ending text");
                var count=vm.Map.Count;vm.Run("eao_n1_close");vm.Run("eao_n1_escort");Require(vm.Map.Count==count&&vm.Items.Count==0,"duplicate rewards/state");
            });
            Test("night-audit-requires-causeway-and-correct-plan",vm=> {
                ReadyNight(vm);vm.Run("eao_n1_plan_audit");Require(vm.Run("eao_n1_tor_commit")==1,"remote hearing");
                vm.Run("eao_n1_plan_shelter");vm.CurrentRoom=vm.RoomIndex("r_eao_n1_yard");Require(vm.Run("eao_n1_tor_commit")==1,"wrong plan signed");
            });
            Test("night-audit-outcome-and-distinct-epilogue",vm=> {
                ReadyNight(vm);vm.Run("eao_n1_plan_audit");vm.CurrentRoom=vm.RoomIndex("r_eao_n1_yard");vm.Run("eao_n1_tor_commit");
                Require((string)vm.Map["EAO_N1_families"]! == "registered"&&(string)vm.Map["EAO_N1_ivo"]! == "held","audit consequences");
                Require(vm.Run("eao_n1_plan_shelter")==1,"committed audit change");
                Require(vm.Run("eao_n1_close")==2&&vm.Run("eao_n1_mara_resume")==4&&vm.Run("eao_n1_tor_resume")==2,"distinct audit ending");
            });
            Test("night-resume-after-commit-without-automatic-completion",vm=> {
                ReadyNight(vm);vm.Run("eao_n1_plan_audit");vm.CurrentRoom=vm.RoomIndex("r_eao_n1_yard");vm.Run("eao_n1_tor_commit");
                Require(vm.Run("eao_n1_mara_resume")==2&&NumberValue(vm.Map["EAO_N1_stage"])==4,"missing return conversation");
                Require(!vm.Map.ContainsKey("EAO_N1_lead"),"automatic lead award");
            });
            Test("night-incomplete-job-cannot-close",vm=> {
                vm.Run("eao_n1_accept");Require(vm.Run("eao_n1_close")==1&&NumberValue(vm.Map["EAO_N1_stage"])==1&&!vm.Map.ContainsKey("EAO_N1_lead"),"premature close");
            });
        }
        return passed.ToArray();
    }
    private static double NumberValue(object? value) => Convert.ToDouble(value, CultureInfo.InvariantCulture);

    private sealed class Paper(int resource) { public int Resource = resource; public bool Carried; }
    private sealed class Vm(Dictionary<string, string> methods, int[] objects, int inventoryObject, UndertaleData data)
    {
        public readonly Dictionary<string, object?> Map = new();
        public readonly Dictionary<int, Paper> Items = new();
        public int Capacity = 4, FailCreation = -1;
        public bool Combat, Dungeon, Changer, FailTransition, Border, MissingRoom, Locked, Drag;
        public bool Dev, Shift;
        public bool WaterLanding, AllWater, WaterPending;
        public int PlaceholderDelays;
        public readonly Dictionary<string,object?> Globals = new() { ["global.EAO_dev_warp_keep"]=false };
        public string DialogText="";
        public bool PlayerExists=true, AbstractExists, FastExists, LandingObstacles, NoLanding;
        public double SpawnX=-50, SpawnY=-50;
        public bool EntryExists, EntryLocked;
        public int EntryCreations, EntryDepth;
        public string EntryName="";
        public int GuiState=2, NativeFallbacks, DoorTarget=-1;
        public bool NativeDoorCreatesChanger;
        public double MapScale=0.5;
        public int CurrentRoom = data.Rooms.ToList().FindIndex(r=>r.Name.Content=="r_taverninside1floor"), RequestedRoom=-4;
        public int GridX=29, GridY=15;
        public string PositionTag="NA";
        public int RoomIndex(string name)=>data.Rooms.ToList().FindIndex(r=>r.Name.Content==name);
        private int ObjectIndex(string name)=>data.GameObjects.ToList().FindIndex(o=>o.Name.Content==name);
        private int nextId = 200000, creations;
        public int State => Map.TryGetValue("EAO_MQ01", out var value) ? (int)Number(value) : 0;
        public int Carried => Items.Values.Count(p => p.Carried);
        public void ReadOriginals() { foreach (var id in new[] { "letter", "enclosure", "receipt" }) Map["EAO_read_eao_" + id] = 1; }
        private static double Number(object? value) => value is bool flag ? (flag ? 1 : 0) : Convert.ToDouble(value, CultureInfo.InvariantCulture);
        private static bool Truth(object? value) => Number(value) >= 0.5; // GML numeric boolean conversion (noone=-4 is false).
        public double Run(string method)
        {
            var lines = methods[method].Split('\n').Select(s => s.Trim()).Where(s => s.Length != 0 && !s.StartsWith('>') && !s.StartsWith(".localvar")).ToArray();
            var labels = new Dictionary<string, int>();
            for (int i = 0; i < lines.Length; i++) if (lines[i].StartsWith(":[")) labels[lines[i][1..]] = i;
            var locals = new Dictionary<string, object?>();
            var stack = new Stack<object?>();
            object? Resolve(string name) {
                if (name == "global.characterDataMap") return Map;
                if (name == "global.language") return 3;
                if (name == "global.guiMouseX") return 256;
                if (name == "global.guiMouseY") return 278;
                if (name == "global.contract_test") return false;
                if (name == "global.EAO_dev_enabled") return Dev;
                if (name == "global.worldWidth") return 50;
                if (name == "global.worldHeight") return 45;
                if (Globals.TryGetValue(name,out var globalValue)) return globalValue;
                if (name == "self.guiInteractiveState") return GuiState;
                if (name == "self.drag") return Drag;
                if (name == "self.edge") return false;
                if (name == "self.enter") return true;
                if (name == "self.guiParent") return 400001;
                if (name is "self.x" or "builtin.x") return 100;
                if (name is "self.y" or "builtin.y") return 200;
                if (name == "builtin.room") return CurrentRoom;
                if (name is "builtin.room_width" or "builtin.room_height") return 312;
                if (name == ObjectIndex("o_controller")+".newgrid") return 999;
                if (name == "global.playerGridX") return GridX;
                if (name == "global.playerGridY") return GridY;
                if (name == "self.test_guide_id") return 200005;
                if (name.StartsWith("[stacktop]self.")) {
                    var receiver=Number(stack.Pop()); if(receiver==-9) receiver=Number(stack.Pop());
                    var field=name["[stacktop]self.".Length..];
                    if(receiver==400001) return field switch {"mapScale"=>MapScale,"mapOffsetX"=>520,"mapOffsetY"=>260,_=>throw new InvalidDataException("Unknown map field: "+name)};
                    if(receiver!=100001) throw new InvalidDataException("Unexpected test player receiver");
                    return field switch { "lock_turn"=>0, "HP"=>100, "x"=>325, "y"=>454, _=>throw new InvalidDataException("Unknown test player field: "+name) };
                }
                if (name.StartsWith("local.")) return locals[name[6..]];
                if (name == "builtin.undefined") return null;
                throw new InvalidDataException("Unsupported callback variable: " + name);
            }
            int steps = 0;
            var stepLimit=method=="test_arrival"?150000:10000;
            for (int pc = 0; pc < lines.Length && steps++ < stepLimit; pc++) {
                var line = lines[pc];
                if (line.StartsWith(":")) continue;
                var split = line.IndexOf(' ');
                var opcode = split < 0 ? line : line[..split];
                var operand = split < 0 ? "" : line[(split + 1)..];
                if (opcode == "setowner.e") continue; // array ownership metadata
                if (opcode is "b" or "bf" or "bt") {
                    bool branch = opcode == "b" || (Truth(stack.Pop()) == (opcode == "bt"));
                    if (branch) pc = labels[operand];
                } else if (opcode.StartsWith("push")) {
                    if (opcode == "push.s") stack.Push(JsonSerializer.Deserialize<string>(operand[..operand.LastIndexOf('@')]));
                    else if (opcode.EndsWith(".v")) stack.Push(Resolve(operand));
                    else stack.Push(double.Parse(operand, CultureInfo.InvariantCulture));
                } else if (opcode.StartsWith("pop.")) {
                    if (method=="test_geo_return" && operand=="self.target") DoorTarget=(int)Number(stack.Pop());
                    else if (operand=="global.position_tag") PositionTag=(string)stack.Pop()!;
                    else if(method=="test_commit" && operand=="global.playerGridX") GridX=(int)Number(stack.Pop());
                    else if(method=="test_commit" && operand=="global.playerGridY") GridY=(int)Number(stack.Pop());
                    else if ((method=="test_execute"||method=="test_arrival")&&operand.StartsWith("global.EAO_dev_warp_")) Globals[operand]=stack.Pop();
                    else if (operand.StartsWith("local.")) locals[operand[6..]] = stack.Pop();
                    else if(method=="test_annex_gate" && operand=="self.is_lock") EntryLocked=Truth(stack.Pop());
                    else if(method=="test_annex_gate" && operand=="self.depth") EntryDepth=(int)Number(stack.Pop());
                    else if(method=="test_annex_gate" && operand=="self.name") EntryName=(string)stack.Pop()!;
                    else if(method=="test_annex_gate" && operand is "self.LVL" or "self.speech_key") stack.Pop();
                    else if(method=="test_arrival" && operand.StartsWith("[stacktop]self.")) {
                        var receiver=Number(stack.Pop());if(receiver==-9) receiver=Number(stack.Pop());
                        if(receiver!=300001) throw new InvalidDataException("Arrival moved a live player instead of a native placeholder.");
                        var value=Number(stack.Pop());
                        if(operand=="[stacktop]self.x") SpawnX=value;
                        else if(operand=="[stacktop]self.y") SpawnY=value;
                        else throw new InvalidDataException("Unexpected arrival field write: "+operand);
                    }
                    else if(method=="test_arrival" && operand=="[array]self.alarm") {
                        var index=Number(stack.Pop());var receiver=Number(stack.Pop());if(receiver==-9) receiver=Number(stack.Pop());var value=Number(stack.Pop());
                        if(receiver!=300001||index is not (0 or 1)||value!=2) throw new InvalidDataException("Invalid placeholder delay");
                        PlaceholderDelays++;
                    }
                    else throw new InvalidDataException("Unexpected callback write: " + operand);
                } else if (opcode == "popz.v") stack.Pop();
                else if (opcode.StartsWith("conv.")) {
                    var value = stack.Pop(); stack.Push(opcode.EndsWith(".b") ? Truth(value) : value);
                } else if (opcode.StartsWith("cmp.")) {
                    var right = stack.Pop(); var left = stack.Pop();
                    bool equal = left is string || right is string ? Equals(left, right) : Number(left) == Number(right);
                    stack.Push(operand switch { "EQ" => equal, "NEQ" => !equal, "LT" => Number(left) < Number(right), "GTE" => Number(left) >= Number(right), "GT" => Number(left) > Number(right), "LTE" => Number(left) <= Number(right), _ => throw new InvalidDataException("Unknown comparison") });
                } else if (opcode.StartsWith("add.")) { var right = stack.Pop(); stack.Push(Number(stack.Pop()) + Number(right)); }
                else if (opcode.StartsWith("sub.")) { var right = stack.Pop(); stack.Push(Number(stack.Pop()) - Number(right)); }
                else if (opcode.StartsWith("mul.")) { var right=stack.Pop();stack.Push(Number(stack.Pop())*Number(right)); }
                else if (opcode.StartsWith("div.")) { var right=stack.Pop();stack.Push(Number(stack.Pop())/Number(right)); }
                else if (opcode.StartsWith("not.")) stack.Push(!Truth(stack.Pop()));
                else if (opcode.StartsWith("ret.")) return Number(stack.Pop());
                else if (opcode.StartsWith("exit.")) return 0;
                else if (opcode == "call.i") {
                    var match = Regex.Match(operand, @"^(\S+)\(argc=(\d+)\)$");
                    var arguments = Enumerable.Range(0, int.Parse(match.Groups[2].Value)).Select(_ => stack.Pop()).ToArray();
                    stack.Push(Call(match.Groups[1].Value.Replace("gml_Script_", ""), arguments));
                } else throw new InvalidDataException("Unsupported compiled callback opcode: " + line);
            }
            if(method.StartsWith("test_") && steps<stepLimit) return 0; // Native event falls through at its end.
            throw new InvalidDataException("Compiled callback did not terminate.");
        }
        private object? Call(string name, object?[] args)
        {
            int Int(int i) => (int)Number(args[i]);
            var paperObject = args.Length > 0 && args[0] is double or int or long ? Int(0) : -1;
            switch (name) {
                case "event_inherited": if (NativeDoorCreatesChanger) Changer=true; return null;
                case "instance_create_depth":
                    if(Int(0)!=351 || Int(1)!=428 || Int(2)!=-1100 || Int(3)!=ObjectIndex("o_eao_d01_entry")) throw new InvalidDataException("Unexpected customs entrance placement");
                    EntryExists=true;EntryCreations++;return 300002;
                case "variable_global_exists": return true;
                case "ds_exists": return true;
                case "scr_actionsLogAddMessage": return null;
                case "audio_play_sound": return 0;
                case "event_user": if(Int(0)!=15) throw new InvalidDataException("Unexpected native map fallback");NativeFallbacks++;return null;
                case "floor": return Math.Floor(Number(args[0]));
                case "keyboard_check": return Shift;
                case "keyboard_check_pressed": return Shift;
                case "get_string": return DialogText;
                case "string_replace_all": return ((string)args[0]!).Replace((string)args[1]!, (string)args[2]!);
                case "string_pos": return ((string)args[1]!).IndexOf((string)args[0]!,StringComparison.Ordinal)+1;
                case "string_length": return ((string)args[0]!).Length;
                case "string_copy": return ((string)args[0]!).Substring(Int(1)-1,Int(2));
                case "string_digits": return new string(((string)args[0]!).Where(c=>c>='0'&&c<='9').ToArray());
                case "real": return double.Parse((string)args[0]!,CultureInfo.InvariantCulture);
                case "is_real": return args[0] is double or int or long or Dictionary<string,object?>; // symbolic DS-map handle
                case "abs": return Math.Abs(Number(args[0]));
                case "astar_get_cell":
                    if(Int(0)!=999) throw new InvalidDataException("Arrival must query the generated native collision grid.");
                    if(NoLanding) return 1;
                    if(!LandingObstacles) return 0;
                    return (Int(1),Int(2)) is (6,6) or (4,6) or (4,7) or (6,4) or (6,3) or (8,6) or (9,6) ? 0 : 1;
                case "scr_check_collision_not_enemy_around": return LandingObstacles&&Int(0)==104;
                case "scr_water_full_filter": return !AllWater&&(!WaterLanding||Int(2)>156);
                case "scr_tile_mark_get_instance": return LandingObstacles&&Int(1)==4?400002:-4;
                case "scr_globalmapIsBorder": return Border;
                case "scr_globaltile_get_room": return MissingRoom?-1:RoomIndex("r_DockStore1floor");
                case "scr_unitTurnGetTime": return false;
                case "scr_getAgredMobsCount": return Combat?1:0;
                case "ds_list_empty": return !Locked;
                case "room_exists": return paperObject>=0&&paperObject<data.Rooms.Count;
                case "room_get_name": return data.Rooms[paperObject].Name.Content;
                case "asset_get_index": return RoomIndex((string)args[0]!);
                case "scr_smoothRoomChange":
                    var events=(List<object?>)args[1]!;
                    if((events.Count==1 ? !(NoLanding||AllWater)||PlayerExists||Number(events[0])!=10 : events.Count!=2||Number(events[0])!=4||Number(events[1])!=10) || Int(2)!=-1 || !Truth(args[3])) throw new InvalidDataException("Native test transition dropped its source saver / coordinate commit order");
                    if(FailTransition) return -4; RequestedRoom=paperObject; Changer=true; return 200006;
                case "scr_atr_set_simple": Map[(string)args[0]!]=args[1]; return null;
                case "ds_map_exists": return ((Dictionary<string, object?>)args[0]!).ContainsKey((string)args[1]!);
                case "ds_map_find_value": return ((Dictionary<string, object?>)args[0]!)[(string)args[1]!];
                case "ds_map_set": ((Dictionary<string, object?>)args[0]!)[(string)args[1]!] = args[2]; return null;
                case "@@NewGMLArray@@": return args.ToList();
                case "array_create": return new List<object?>();
                case "array_get": return ((List<object?>)args[0]!)[Int(1)];
                case "array_length": return ((List<object?>)args[0]!).Count;
                case "array_push": ((List<object?>)args[0]!).AddRange(args.Skip(1)); return null;
                case "instance_find":
                    if(paperObject==ObjectIndex("o_abstract_player")) return AbstractExists?300001:-4;
                    if(paperObject==ObjectIndex("o_fastTurnController")) return FastExists?300001:-4;
                    if(paperObject==ObjectIndex("o_player")&&Int(1)==0) return 100001;
                    if (paperObject != inventoryObject || Int(1) != 0) throw new InvalidDataException("Wrong inventory receiver"); return 100000;
                case "instance_exists":
                    if(paperObject==ObjectIndex("o_water_grid")) return WaterPending;
                    if(paperObject==ObjectIndex("o_eao_d01_entry")) return EntryExists;
                    if(paperObject==ObjectIndex("o_globalmap")||paperObject==ObjectIndex("o_journal")||paperObject==ObjectIndex("o_dialogue")) return false;
                    if(paperObject==ObjectIndex("o_dungeon_controller")) return Dungeon;
                    if(paperObject==ObjectIndex("o_smoothRoomChanger")) return Changer;
                    if(paperObject==ObjectIndex("o_controller")) return true;
                    if(paperObject==ObjectIndex("o_player")) return PlayerExists;
                    if(paperObject==300001) return AbstractExists||FastExists;
                    if(paperObject==400002) return LandingObstacles;
                    return paperObject is 100000 or 100001 or 400001 || (paperObject==200006&&Changer) || Items.ContainsKey(paperObject);
                case "scr_instance_exists_item": return Items.Values.Count(p => p.Resource == paperObject && (Int(3) == 0 || p.Carried));
                case "scr_inventory_add_item":
                    if (Int(1) != 100000 || Truth(args[5]) || !objects.Contains(paperObject)) throw new InvalidDataException("Auto-drop or receiver regression");
                    if (++creations == FailCreation) return -4;
                    var id = nextId++; Items.Add(id, new Paper(paperObject)); return id;
                case "scr_inventory_add":
                    if (Int(0) != 100000) throw new InvalidDataException("Placement receiver regression");
                    if (Carried >= Capacity) return false; Items[Int(1)].Carried = true; return true;
                case "scr_item_destroy": Items.Remove(Int(0)); return null;
                default: throw new InvalidDataException("Unsupported native test double: " + name);
            }
        }
    }
}

