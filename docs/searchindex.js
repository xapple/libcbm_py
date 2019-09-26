Search.setIndex({docnames:["cbm_core_functions","cbm_input_and_variables","cbm_model","cbm_sit","cbm_testing","index","libcbm_core_functions","other_functions","sit_example"],envversion:{"sphinx.domains.c":1,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":1,"sphinx.domains.javascript":1,"sphinx.domains.math":2,"sphinx.domains.python":1,"sphinx.domains.rst":1,"sphinx.domains.std":1,nbsphinx:1,sphinx:56},filenames:["cbm_core_functions.rst","cbm_input_and_variables.rst","cbm_model.rst","cbm_sit.rst","cbm_testing.rst","index.rst","libcbm_core_functions.rst","other_functions.rst","sit_example.ipynb"],objects:{"libcbm.data_helpers":{append_simulation_result:[7,1,1,""],get_ndarray:[7,1,1,""],get_nullable_ndarray:[7,1,1,""],promote_scalar:[7,1,1,""],unpack_ndarrays:[7,1,1,""]},"libcbm.input.sit":{sit_age_class_parser:[3,0,0,"-"],sit_cbm_factory:[3,0,0,"-"],sit_classifier_parser:[3,0,0,"-"],sit_disturbance_event_parser:[3,0,0,"-"],sit_disturbance_type_parser:[3,0,0,"-"],sit_format:[3,0,0,"-"],sit_inventory_parser:[3,0,0,"-"],sit_parser:[3,0,0,"-"],sit_reader:[3,0,0,"-"],sit_transition_rule_parser:[3,0,0,"-"],sit_yield_parser:[3,0,0,"-"]},"libcbm.input.sit.sit_age_class_parser":{generate_sit_age_classes:[3,1,1,""],parse:[3,1,1,""]},"libcbm.input.sit.sit_cbm_factory":{get_classifiers:[3,1,1,""],get_merch_volumes:[3,1,1,""],initialize_cbm:[3,1,1,""],initialize_inventory:[3,1,1,""],initialize_sit_objects:[3,1,1,""],load_sit:[3,1,1,""],read_sit_config:[3,1,1,""]},"libcbm.input.sit.sit_classifier_parser":{get_classifier_keyword:[3,1,1,""],get_wildcard_keyword:[3,1,1,""],parse:[3,1,1,""]},"libcbm.input.sit.sit_disturbance_event_parser":{get_sort_types:[3,1,1,""],get_target_types:[3,1,1,""],parse:[3,1,1,""]},"libcbm.input.sit.sit_disturbance_type_parser":{parse:[3,1,1,""]},"libcbm.input.sit.sit_format":{get_age_class_format:[3,1,1,""],get_age_eligibility_columns:[3,1,1,""],get_classifier_format:[3,1,1,""],get_disturbance_eligibility_columns:[3,1,1,""],get_disturbance_event_format:[3,1,1,""],get_disturbance_type_format:[3,1,1,""],get_inventory_format:[3,1,1,""],get_transition_rule_classifier_set_postfix:[3,1,1,""],get_transition_rules_format:[3,1,1,""],get_yield_format:[3,1,1,""]},"libcbm.input.sit.sit_inventory_parser":{expand_age_class_inventory:[3,1,1,""],get_map_land_class_func:[3,1,1,""],parse:[3,1,1,""]},"libcbm.input.sit.sit_mapping":{SITMapping:[3,2,1,""]},"libcbm.input.sit.sit_mapping.SITMapping":{get_disturbance_type_id:[3,3,1,""],get_land_class_id:[3,3,1,""],get_spatial_unit:[3,3,1,""],get_species:[3,3,1,""]},"libcbm.input.sit.sit_parser":{get_parse_bool_func:[3,1,1,""],substitute_using_age_class_rows:[3,1,1,""],unpack_column:[3,1,1,""],unpack_table:[3,1,1,""]},"libcbm.input.sit.sit_reader":{load_table:[3,1,1,""],parse:[3,1,1,""]},"libcbm.input.sit.sit_transition_rule_parser":{parse:[3,1,1,""]},"libcbm.input.sit.sit_yield_parser":{parse:[3,1,1,""]},"libcbm.model.cbm":{cbm_defaults:[1,0,0,"-"],cbm_defaults_queries:[1,0,0,"-"],cbm_factory:[2,0,0,"-"],cbm_simulator:[2,0,0,"-"]},"libcbm.model.cbm.cbm_config":{classifier:[1,1,1,""],classifier_config:[1,1,1,""],classifier_value:[1,1,1,""],merch_volume_curve:[1,1,1,""],merch_volume_to_biomass_config:[1,1,1,""]},"libcbm.model.cbm.cbm_defaults":{get_cbm_parameters_factory:[1,1,1,""],get_libcbm_configuration_factory:[1,1,1,""],load_cbm_flux_indicators:[1,1,1,""],load_cbm_parameters:[1,1,1,""],load_cbm_pools:[1,1,1,""]},"libcbm.model.cbm.cbm_defaults_queries":{get_query:[1,1,1,""],get_script_dir:[1,1,1,""]},"libcbm.model.cbm.cbm_defaults_reference":{CBMDefaultsReference:[1,2,1,""]},"libcbm.model.cbm.cbm_defaults_reference.CBMDefaultsReference":{get_afforestation_pre_type_id:[1,3,1,""],get_afforestation_pre_types:[1,3,1,""],get_disturbance_type_id:[1,3,1,""],get_disturbance_types:[1,3,1,""],get_flux_indicators:[1,3,1,""],get_land_class_by_disturbance_type:[1,3,1,""],get_land_class_disturbance_ref:[1,3,1,""],get_land_class_id:[1,3,1,""],get_land_classes:[1,3,1,""],get_pools:[1,3,1,""],get_spatial_unit:[1,3,1,""],get_spatial_unit_id:[1,3,1,""],get_spatial_units:[1,3,1,""],get_species:[1,3,1,""],get_species_id:[1,3,1,""],load_data:[1,3,1,""]},"libcbm.model.cbm.cbm_factory":{create:[2,1,1,""]},"libcbm.model.cbm.cbm_model":{CBM:[2,2,1,""]},"libcbm.model.cbm.cbm_model.CBM":{init:[2,3,1,""],spinup:[2,3,1,""],step:[2,3,1,""]},"libcbm.model.cbm.cbm_simulator":{create_in_memory_reporting_func:[2,1,1,""],simulate:[2,1,1,""]},"libcbm.model.cbm.cbm_variables":{initialize_cbm_parameters:[1,1,1,""],initialize_cbm_state_variables:[1,1,1,""],initialize_flux:[1,1,1,""],initialize_inventory:[1,1,1,""],initialize_pools:[1,1,1,""],initialize_spinup_parameters:[1,1,1,""],initialize_spinup_variables:[1,1,1,""]},"libcbm.test.cbm":{case_generation:[4,0,0,"-"],flux_comparison:[4,0,0,"-"],pool_comparison:[4,0,0,"-"],result_comparison:[4,0,0,"-"],state_comparison:[4,0,0,"-"],test_case_simulator:[4,0,0,"-"]},"libcbm.test.cbm.case_generation":{generate_scenarios:[4,1,1,""],get_classifier_value_name:[4,1,1,""],get_expCurve_func:[4,1,1,""],get_ramp_func:[4,1,1,""],get_random_sigmoid_func:[4,1,1,""],get_step_func:[4,1,1,""]},"libcbm.test.cbm.cbm3_support":{cbm3_python_helper:[4,0,0,"-"],cbm3_simulator:[4,0,0,"-"]},"libcbm.test.cbm.cbm3_support.cbm3_python_helper":{load_cbm3_python:[4,1,1,""]},"libcbm.test.cbm.cbm3_support.cbm3_simulator":{get_cbm3_results:[4,1,1,""],get_config_path:[4,1,1,""],get_project_path:[4,1,1,""],get_results_path:[4,1,1,""],get_unfccc_land_class_id_ref:[4,1,1,""],import_cbm3_project:[4,1,1,""],run_cbm3:[4,1,1,""]},"libcbm.test.cbm.flux_comparison":{get_cbm3_annual_process_flux:[4,1,1,""],get_cbm3_disturbance_flux:[4,1,1,""],get_cbm3_flux_annual_process_cols:[4,1,1,""],get_cbm3_flux_disturbance_cols:[4,1,1,""],get_libcbm_flux_annual_process_cols:[4,1,1,""],get_libcbm_flux_disturbance_cols:[4,1,1,""],get_merged_annual_process_flux:[4,1,1,""],get_merged_disturbance_flux:[4,1,1,""]},"libcbm.test.cbm.pool_comparison":{get_cbm3_biomass_pools:[4,1,1,""],get_cbm3_dom_pools:[4,1,1,""],get_cbm3_pools:[4,1,1,""],get_libcbm_biomass_pools:[4,1,1,""],get_libcbm_dom_pools:[4,1,1,""],get_libcbm_pools:[4,1,1,""],get_merged_pools:[4,1,1,""],get_pool_map:[4,1,1,""],prepare_cbm3_pools:[4,1,1,""]},"libcbm.test.cbm.result_comparison":{diff_result:[4,1,1,""],get_summarized_diff_plot:[4,1,1,""],get_test_case_comparison_by_indicator_plot:[4,1,1,""],get_test_case_comparison_plot:[4,1,1,""],merge_result:[4,1,1,""],summarize_diffs_by_identifier:[4,1,1,""]},"libcbm.test.cbm.state_comparison":{get_merged_state:[4,1,1,""],prepare_cbm3_state:[4,1,1,""]},"libcbm.test.cbm.test_case_simulator":{get_classifier_value_lookup:[4,1,1,""],get_disturbances:[4,1,1,""],get_test_case_classifier_factory:[4,1,1,""],get_test_case_merch_volume_factory:[4,1,1,""],initialize_inventory:[4,1,1,""],run_test_cases:[4,1,1,""]},"libcbm.wrapper.cbm":{cbm_ctypes:[0,0,0,"-"]},"libcbm.wrapper.cbm.cbm_ctypes":{initialize_CBM_ctypes:[0,1,1,""]},"libcbm.wrapper.cbm.cbm_wrapper":{CBMWrapper:[0,2,1,""]},"libcbm.wrapper.cbm.cbm_wrapper.CBMWrapper":{AdvanceSpinupState:[0,3,1,""],AdvanceStandState:[0,3,1,""],EndSpinupStep:[0,3,1,""],EndStep:[0,3,1,""],GetDecayOps:[0,3,1,""],GetDisturbanceOps:[0,3,1,""],GetMerchVolumeGrowthOps:[0,3,1,""],GetTurnoverOps:[0,3,1,""],InitializeLandState:[0,3,1,""]},"libcbm.wrapper.cbm.libcbm_spinup_state":{LibCBM_SpinupState:[0,2,1,""]},"libcbm.wrapper.cbm.libcbm_spinup_state.LibCBM_SpinupState":{get_name:[0,3,1,""]},"libcbm.wrapper.libcbm_ctypes":{LibCBM_ctypes:[6,2,1,""]},"libcbm.wrapper.libcbm_error":{LibCBM_Error:[6,2,1,""]},"libcbm.wrapper.libcbm_error.LibCBM_Error":{getError:[6,3,1,""],getErrorMessage:[6,3,1,""]},"libcbm.wrapper.libcbm_handle":{LibCBMHandle:[6,2,1,""]},"libcbm.wrapper.libcbm_handle.LibCBMHandle":{call:[6,3,1,""]},"libcbm.wrapper.libcbm_matrix":{LibCBM_Matrix:[6,2,1,""],LibCBM_Matrix_Base:[6,2,1,""],LibCBM_Matrix_Int:[6,2,1,""]},"libcbm.wrapper.libcbm_wrapper":{LibCBMWrapper:[6,2,1,""]},"libcbm.wrapper.libcbm_wrapper.LibCBMWrapper":{AllocateOp:[6,3,1,""],ComputeFlux:[6,3,1,""],ComputePools:[6,3,1,""],FreeOp:[6,3,1,""],SetOp:[6,3,1,""]},libcbm:{data_helpers:[7,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","function","Python function"],"2":["py","class","Python class"],"3":["py","method","Python method"]},objtypes:{"0":"py:module","1":"py:function","2":"py:class","3":"py:method"},terms:{"0x1a3ed64ab88":8,"0x1a3ed697148":8,"0x1a3efc3d4c8":8,"0x1cad07edf48":[],"0x1cad30e6a48":[],"0x20edf474e88":[],"0x2cc30b8c088":[],"0x2cc30d76a08":[],"0x2cc32a53d88":[],"boolean":3,"case":[2,5,7],"class":[0,1,4,5,6,7],"default":[0,2,3,4,5,6,7,8],"enum":0,"final":1,"float":6,"function":[1,2,3,5,8],"import":[2,4,5],"int":[0,1,2,3,4,6,7],"new":[5,7],"null":[7,8],"return":[0,1,2,3,4,6,7],"static":0,"true":[0,2,3,4,8],Age:[4,5],For:[1,3,4,6,7],Ids:6,The:[0,1,4,5,6,7,8],These:1,Use:[1,3],Used:[0,1,3,6],Will:[0,2],With:[2,3],_classifi:3,_subplot:8,abbrevi:3,abil:2,about:1,abov:[1,2],abovegroundfastsoil:8,abovegroundslowsoil:8,abovegroundveryfastsoil:8,abs_total_diff:4,absolut:3,abspath:8,accept:2,access:[1,2,4,5],accord:[3,4,6],act:3,actual:3,added:7,addit:[4,5],admin:1,admin_boundary_nam:1,advanc:[0,2],advancespinupst:0,advancestandst:0,afforest:[0,1,2,4],afforestation_pre_type_id:1,afforestation_pre_type_nam:1,after:[0,2],age0:0,age1:0,age:[1,3,4,8],age_0:[3,8],age_10:8,age_1:[3,8],age_2:[3,8],age_3:[3,8],age_4:[3,8],age_5:[3,8],age_6:[3,8],age_7:[3,8],age_8:[3,8],age_9:[3,8],age_class:[3,8],age_class_t:3,age_interv:[3,4],age_volume_pair:[0,1,2],agen:0,ages:3,agg1:3,agg2:3,aggreg:3,aggregate_valu:3,align:1,all:[0,1,2,3,4,6],alloc:[0,2,5,6],allocateop:[0,6],allow:[2,7],along:1,alreadi:[4,7],also:[0,4,5,6,8],alter:[0,1,2,4],analysi:4,ani:[1,3,4,6],annual:[0,1,4],annual_process_flux:8,api:2,appear:3,append:[2,3,4,7,8],append_simulation_result:7,appendix:5,appli:0,applic:4,approach:4,appropri:[0,6],archiv:4,archive_index_db_path:4,area:[3,8],arg:[3,4,6],argument:[0,1,6,7],arrai:[2,4,6,7],assertionerror:[1,6],assign:[3,6],associ:[0,1,3,4],assum:[4,6],attach:3,autom:4,avail:1,averag:4,axes:8,axessubplot:[4,8],axi:4,base:[0,1,3,4,5,6],base_index:3,basi:[1,2],becaus:3,befor:0,being:3,belowgroundfastsoil:8,belowgroundslowsoil:8,belowgroundveryfastsoil:8,between:[1,2,3,4,6],biomass:[0,2,4],biomass_pool:8,biomass_turnover_op:0,bit:[5,6],block:[0,6],bool:[0,2,3,4],both:[1,2,3,4],boundari:1,branch:4,built:2,bulk:0,burn:8,c1_v1:[1,2],c1_v2:1,c1_v5:1,c1_vk:1,c1_vn:1,c2_v1:1,c2_v2:1,c2_vk:1,c_contigu:6,c_doubl:7,call:[0,2,3,6],caller:2,can:[1,2,4,6,7],captur:1,carbon:[2,4],carri:3,case_gener:4,case_index_0:4,case_index_k:4,casegener:4,cat:[1,4],caus:[1,4],cb3_python:4,cbm3:4,cbm3_flux:4,cbm3_pool:4,cbm3_project_path:4,cbm3_python:4,cbm3_python_help:4,cbm3_result:4,cbm3_results_db_path:4,cbm3_simul:4,cbm3_state:4,cbm3_support:4,cbm:[5,6,8],cbm_config:[0,1,2,3],cbm_ctype:0,cbm_default:[0,1,2,3,4],cbm_defaults_db_path:[],cbm_defaults_queri:1,cbm_defaults_ref:[3,4],cbm_defaults_refer:1,cbm_exe_path:4,cbm_factori:[1,2],cbm_model:[1,2,3],cbm_parameters_factori:2,cbm_simul:[2,8],cbm_var:[],cbm_variabl:[0,1,2],cbm_wrapper:[0,1,2],cbmdefaultsrefer:[1,4],cbmwrapper:[0,1,2],cell:6,celsiu:1,certain:7,cfs3:[2,3,5],cfs:[1,4],ch4:8,chang:[0,1,3,4],chapter:3,check:3,cj_v1:1,cj_v2:1,cj_vi:1,ck_vx:1,class_siz:[3,8],classifi:[0,2,4,5,8],classifier1:3,classifier2:3,classifier_1:1,classifier_2:1,classifier_3:1,classifier_aggreg:3,classifier_config:[1,2,3],classifier_id:[0,1,3,8],classifier_nam:[3,4],classifier_set:[0,1,2],classifier_valu:[0,1,2,3,8],classifiers_factori:2,classifiers_t:3,clear:8,clearcut:[3,8],clone:4,co2:8,coarsetoair:4,code:[0,1,3,6,8],collect:[1,4,6],colmun:3,colnam:3,column:[1,2,3,4,6,7,8],column_descript:3,com:[1,4],combin:[1,4,6],compar:[2,4],comparison:5,compat:[0,1,2],compil:[1,2,3,4,5,6],complic:3,compon:[0,1,4],compos:[0,1,2],compris:[0,2],comput:[0,3,5,6],compute_funct:2,computeflux:6,computepool:6,conceptu:6,condit:[1,4],config:[0,3,4,6,8],config_dir:3,config_fil:[],config_path:[3,8],configur:[0,1,2,3,4,6,8],consist:2,constant:1,constrain:6,constraint:3,construct:[0,2],consum:2,consumpt:[1,4],contain:[0,1,3,4,6],content:[1,5,7],control:[2,5],convent:1,convers:[3,4],convert:[3,4,7],coordin:6,copi:[3,4],core:5,correct:[0,3,6],correspond:[1,4,6],creat:[1,2,3,4,7,8],create_in_memory_reporting_func:[2,8],creation:4,criteria:[0,3],csv:[3,8],ctype:[0,6,7],current:[0,4],curv:[0,2,3,4,5],cut:8,data:[0,1,2,3,4,6,7],data_help:7,databas:[1,3,4],datafram:[0,1,2,3,4,6,7,8],dataset:[3,8],db_path:[0,1,2,3,4],dead:[0,4],deal:7,dealloc:6,debug:[2,4],decai:0,decaydomco2emiss:8,decayfastagtoair:8,decayfastbgtoair:8,decayhwbranchsnagtoair:8,decayhwstemsnagtoair:8,decaymediumtoair:8,decayslowagtoair:8,decayslowbgtoair:8,decayswbranchsnagtoair:8,decayswstemsnagtoair:8,decayvfastagtoair:8,decayvfastbgtoair:8,decim:4,def:[],default_dist_typ:8,default_speci:8,default_spuid:8,defin:[0,1,2,3,4,6,7],definit:[0,2,3,6],deforest:[4,8],degre:1,delai:[3,8],deltabiomass_ag:8,deltabiomass_bg:8,demonstr:[],depend:7,descend:4,describ:[1,2,3],descript:[0,1,3,4,8],detail:3,detect:[3,4,6],develop:5,dict:[1,3,4],dictionari:[1,3,4],did:3,diff:4,diff_result:4,differ:4,dimens:[2,6],dimension:6,dir:4,directori:[1,3,4],dirnam:[],disabl:6,dist1:[3,8],dist2:[3,8],dist3:[3,8],distid1:3,distid2:3,distid3:3,disturb:[0,1,4,5,8],disturbacn:3,disturbance_ev:3,disturbance_op:0,disturbance_typ:[1,3,8],disturbance_type_id:[1,4],disturbance_type_nam:1,disturbance_types_t:3,disturbancebioch4emiss:8,disturbancebioco2emiss:8,disturbancebiocoemiss:8,disturbancech4product:8,disturbanceco2product:8,disturbancecoproduct:8,disturbancefastagtoair:8,disturbancefastbgtoair:8,disturbancehwbranchsnagtoair:8,disturbancehwstemsnagtoair:8,disturbancemediumtoair:8,disturbanceslowagtoair:8,disturbanceslowbgtoair:8,disturbancesoftproduct:8,disturbanceswbranchsnagtoair:8,disturbanceswstemsnagtoair:8,disturbancevfastbgtoair:8,divid:3,dll:[0,2,6],dll_config_factori:2,dll_path:[2,3,4,6],doe:[2,3,4],dom:[0,4],dom_decay_op:0,dom_pool:8,drawn:1,driver:5,drop:4,dtype:7,due:4,dump:8,duplic:3,dure:[0,2,6],dynam:[2,3,4,5],each:[1,2,3,4,6,7,8],easi:4,eco:1,eco_boundary_nam:1,either:[2,6,7],element:6,elig:3,empti:6,enabl:[4,6,8],encod:[3,4],encompass:8,end:0,end_year:[3,8],endspinupstep:0,endstep:0,equal:[1,3],error:[1,3,6],etc:8,event:[0,4,5,8],everi:[1,4],exampl:[0,1,2,3,4,5,6],except:[3,6],exe:4,execut:[1,4],exist:[3,4],exit:0,exp:4,expand:3,expand_age_class_inventori:3,expect:1,explicit:0,exponenti:4,expos:[0,6],extend:[0,5],extern:4,extra:4,factori:[2,4],failur:3,fals:[0,2,3,4],featur:[2,3],feedback:[2,3],fetch:[0,3,4],field:[0,3],figsiz:8,file:[1,3,4,6],fill:[1,7],filter:4,find:0,finetoair:4,finish:0,fire:[3,8],first:3,flow:[0,1,2,6],flux:[2,5,6],flux_comparison:4,flux_ind:[2,6,8],flux_indicator_cod:[1,2,8],follow:[1,2,3,4,6,8],foltoair:4,forest:[1,4,8],forest_type_id:1,forest_type_nam:1,form:4,format:[0,1,4,5,6,8],found:[1,3],frame:2,freeop:6,friendli:3,from:[0,1,2,3,4,6,7,8],full:[2,3,5],fulli:4,func:[1,2,3,4],func_nam:6,gener:[1,3,5,6],generate_scenario:4,generate_sit_age_class:3,genus_id:1,genus_nam:1,get:[0,1,3,4,6,7],get_afforestation_pre_typ:1,get_afforestation_pre_type_id:1,get_age_class_format:3,get_age_eligibility_column:3,get_cbm3_annual_process_flux:4,get_cbm3_biomass_pool:4,get_cbm3_disturbance_flux:4,get_cbm3_dom_pool:4,get_cbm3_flux_annual_process_col:4,get_cbm3_flux_disturbance_col:4,get_cbm3_pool:4,get_cbm3_result:4,get_cbm_parameters_factori:[1,2],get_classifi:3,get_classifier_format:3,get_classifier_keyword:3,get_classifier_value_lookup:4,get_classifier_value_nam:4,get_config_path:4,get_disturb:4,get_disturbance_eligibility_column:3,get_disturbance_event_format:3,get_disturbance_typ:1,get_disturbance_type_format:3,get_disturbance_type_id:[1,3],get_expcurve_func:4,get_flux_ind:[1,8],get_inventory_format:3,get_land_class:1,get_land_class_by_disturbance_typ:1,get_land_class_disturbance_ref:1,get_land_class_id:[1,3],get_libcbm_biomass_pool:4,get_libcbm_configuration_factori:[1,2],get_libcbm_dom_pool:4,get_libcbm_flux_annual_process_col:4,get_libcbm_flux_disturbance_col:4,get_libcbm_pool:4,get_map_land_class_func:3,get_matrix:6,get_merch_volum:3,get_merged_annual_process_flux:4,get_merged_disturbance_flux:4,get_merged_pool:4,get_merged_st:4,get_nam:0,get_ndarrai:7,get_nullable_ndarrai:7,get_parse_bool_func:3,get_pool:[1,8],get_pool_map:4,get_project_path:4,get_queri:1,get_ramp_func:4,get_random_sigmoid_func:4,get_results_path:4,get_script_dir:1,get_sort_typ:3,get_spatial_unit:[1,3],get_spatial_unit_id:1,get_speci:[1,3],get_species_id:1,get_step_func:4,get_summarized_diff_plot:4,get_target_typ:3,get_test_case_classifier_factori:4,get_test_case_comparison_by_indicator_plot:4,get_test_case_comparison_plot:4,get_test_case_merch_volume_factori:4,get_transition_rule_classifier_set_postfix:3,get_transition_rules_format:3,get_unfccc_land_class_id_ref:4,get_wildcard_keyword:3,get_yield_format:3,getdecayop:0,getdisturbanceop:0,geterror:6,geterrormessag:6,getmerchvolumegrowthop:0,getturnoverop:0,git:4,github:[1,4,5],gitpython:5,given:[1,4],gleysol:8,greater:3,group:3,groupbi:8,growth:[0,1,2,4,5],growth_curve_len:4,growth_en:8,growth_multipli:8,growth_onli:[4,8],growth_op:0,handl:[0,6],hardwood:3,hardwoodbranchsnag:8,hardwoodcoarseroot:8,hardwoodfineroot:8,hardwoodfoliag:8,hardwoodmerch:8,hardwoodoth:8,hardwoodstemsnag:8,has:[1,2,3,4,5],have:[0,1,2,3,4,5,6],head:8,header:3,helper:[0,3,7],here:[1,3,4,6],hist_dist:3,histor:[0,1,3],historical_disturbance_typ:[1,3,8],historical_mean_annual_temp:0,how:3,http:[1,4],human:1,ident:[3,4],identifi:[1,3,4,8],ids:[1,3,4,6],ignor:[0,3],implement:[2,8],import_cbm3_project:4,import_config:[3,8],includ:[1,2,3,4,5],inclus:3,incorrect:3,increment:0,indent:8,index:[1,3,4,5,6],indic:[1,2,4,6],info:1,inform:[1,2,4],init:2,initi:[0,1,2,3,4,6,8],initialize_cbm:[3,8],initialize_cbm_ctyp:0,initialize_cbm_paramet:[0,1,2],initialize_cbm_state_vari:[0,1,2],initialize_flux:[1,2],initialize_inventori:[0,1,2,3,4,8],initialize_pool:[1,2],initialize_simulation_vari:2,initialize_sit_object:3,initialize_spinup_paramet:[0,1,2],initialize_spinup_vari:[0,1,2],initializecbm:1,initializelandst:0,inlin:8,input:[4,5,8],instal:4,instanc:[0,2,3,4,6,7,8],integ:[0,3,6,7],integr:2,intend:[0,4],interact:2,interdepend:3,intern:[2,4,6],invalid:[3,4],inventori:[0,2,4,5,8],inventory_t:3,involv:4,issu:3,its:4,join:4,join_result:4,json:[0,3,6,8],jupyt:5,jupytext:5,kei:[1,3,4],keyerror:3,keyword:[1,3],label:[1,3,4],lambda:[2,8],land:[1,3,4],land_class:[1,3,4,8],land_class_cod:1,land_class_descript:1,land_class_id:1,landclass:[1,3,4],landclassid:4,larger:7,last:[0,3],last_dist:3,last_disturbance_typ:8,last_pass_disturbance_typ:[1,3,8],latest:4,layout:2,lc_1:3,lc_2:3,leading_speci:[3,8],least:3,len:6,length:[1,3,6,7],less:3,level:[0,4,6],libcbm:[0,1,2,3,4,7,8],libcbm_ctyp:[0,6],libcbm_error:6,libcbm_flux:4,libcbm_handl:[0,6],libcbm_matrix:6,libcbm_matrix_bas:6,libcbm_matrix_int:6,libcbm_path:[],libcbm_pool:4,libcbm_result:4,libcbm_spinup_st:0,libcbm_spinupst:0,libcbm_stat:4,libcbm_wrapp:[1,2,6],libcbmhandl:[0,6],libcbmwrapp:[1,2,6],librari:[0,1,2,3,4,5,6],lifetim:6,like:[1,3,4,5,6],limit:[0,4],line:8,link:[],linux:6,list:[1,2,3,4,6],liter:3,load:[1,3,4,8],load_cbm3_python:4,load_cbm_flux_ind:1,load_cbm_paramet:1,load_cbm_pool:1,load_data:1,load_set:[],load_sit:[3,8],load_tabl:3,local:4,locale_cod:1,look:4,low:[0,6],mai:6,make:4,makelist:4,mani:2,manual:3,map:[4,5],mapping_config:8,mapping_mod:8,master:4,match:[0,1,3,4],matmul:6,matplotlib:[4,8],matric:[0,6],matrix:[0,5,6],matrix_0:6,matrix_1:6,matrix_c_typ:6,matrix_index:6,matrix_np_typ:6,matter:[0,4],max:3,max_ag:3,max_compon:4,max_disturb:4,max_hardwood_ag:3,max_result:4,max_rot:1,max_softwood_ag:3,max_valu:3,maximum:[1,3,4],mean:[0,1,2],mean_annu:1,mean_annual_temp:1,mediumsoil:8,member:7,memori:[6,7,8],merch:[0,4],merch_volum:[1,2],merch_volume_curv:[0,1,2],merch_volume_to_biomass:0,merch_volume_to_biomass_config:[1,2],merch_volume_to_biomass_factori:2,merchant:[0,2,3,4,5],merchtoair:4,merg:4,merge_result:4,messag:[3,6],metadata:3,method:[0,1,2,3,4,5,6,7],might:1,min:3,min_hardwood_ag:3,min_rot:1,min_softwood_ag:3,min_valu:3,minimum:[1,3],mix:[0,3],mode:3,model:[0,1,2,3,4,5,6,8],model_funct:2,modifi:[0,2],modul:[1,2,5,8],more:[3,4],much:4,multipl:[4,7],must:[1,3,6],my_fil:3,n_column:3,n_flux_ind:[2,6],n_growth_digit:4,n_op:6,n_pool:[0,2,6],n_stand:[0,1,2,6],n_step:[2,4,8],name:[0,1,3,4,6,8],namespac:[3,7],nan:3,ndarrai:[0,1,2,6,7],necessari:[3,7],need:1,neg:[0,1],negat:4,nest:4,next:5,no2:8,non:[0,1,2,8],none:[1,2,3,4,6,7],nonforest:8,note:3,notebook:5,notebook_startup:8,notimplementederror:3,num_age_class:4,num_cas:4,number:[0,1,2,3,4,6,7],numer:4,numpi:[0,1,2,5,6,7],oak:8,object:[0,1,2,3,4,7],occur:[2,3,4,6,7],offer:2,offset:3,omit:4,on_error:3,one:[0,2,3,4,7],onli:[0,2,3,4,5,7,8],onto:3,op_id:6,op_process:6,open:[],oper:[0,3,4,6],ops:6,option:[0,1,2,3,4,6,7],order:[1,2,3,4,5,6],ordereddict:4,organ:[0,4],origin:7,other:[1,2,3,5,6],otherwis:[2,3,4,7],othtoair:4,output:[1,2,3,4],overrid:1,packag:8,page:5,pair:[1,2,3,4,6],panda:[0,1,2,3,4,5,6,7],param:[3,8],paramet:[0,2,3,4,5,6,7,8],parameter:4,parameterless:1,pars:3,parse_age_class:3,parse_bool_func:3,partial:4,particular:8,pass:[0,1,2,3,4,6],path:[1,2,3,4,6,8],pattern:1,per:[1,3],percent:3,perform:[1,4,6],pine:8,place:4,plot:[4,8],plot_kwarg:4,point:4,pointer:7,pool1:1,pool2:1,pool:[0,2,5,6],pool_1:6,pool_2:6,pool_cod:[1,2,8],pool_comparison:4,pool_ind:[2,8],pool_map:4,pool_n:6,pooln:1,poolnam:4,pools_includ:4,possibl:3,post:1,postfix:3,potenti:7,power:2,pre:[0,1,2],pre_dynamics_func:[2,8],prepar:0,prepare_cbm3_pool:4,prepare_cbm3_st:4,present:3,prevent:0,primari:3,print:8,prior:[2,6],problem:3,procedur:1,process:[1,2,3,4,6],process_id:[1,6],produc:[3,4],product:8,project:4,project_path:4,promot:[1,7],promote_scalar:[1,7],properti:[1,2,3,7],provid:[0,1,2,6],pseudocod:6,pull:4,pure:[3,7],purpos:5,pyodbc:5,python3x:5,python:[0,6],queri:[1,4],query_filenam:1,query_param:1,quirk:4,rais:[0,1,3,4,6,7],ramp:4,random:4,random_se:4,randomli:4,rang:3,raw:[4,6],read:[0,1,2,5],read_csv:3,read_sit_config:3,readabl:1,readi:4,record:3,ref:4,refer:[4,5,7],referenc:6,regeneration_delai:[0,8],regular:[0,6],relat:6,relationship:8,renam:4,replic:2,reporting_func:[2,8],repositori:4,repres:3,represent:3,requir:[1,3,4,8],reset_ag:0,result:[1,2,3,4,5,7],result_comparison:4,result_limit:4,return_interv:1,revis:4,rewrit:4,rigor:4,root:0,rotat:1,round:4,rout:0,routin:[0,1],row:[1,2,3,4,6,8],rule:[1,5,6],run:[0,2,3,4,5,8],run_cbm3:4,run_test_cas:4,runtim:1,runtimeerror:6,s_ref:3,same:[0,1,2,3,6],save:4,scalar:[1,6,7],scale:[3,4],scenario:4,scheme:1,scipi:5,script:1,search:5,second:[3,4],section:1,see:[0,1,2,3,4,5],seed:4,select:2,sensibl:4,sep:3,separ:3,seri:[3,7],set:[0,1,2,3,4,6,7],setop:6,setup:5,sever:6,shape:[0,6],side:4,sigmoid:4,similar:4,simplenamespac:[2,3,7],simul:[0,1,5,7],simulation_result:7,simult:2,sinc:[3,4],singl:[2,3,4,6,7],singledefaultspatialunit:8,sink:1,sink_pool:[1,6],sit:[4,5],sit_age_class:[3,8],sit_age_class_pars:3,sit_ageclass:3,sit_cbm_factori:[3,8],sit_classifi:[3,8],sit_classifier_pars:3,sit_config:8,sit_config_save_path:4,sit_data:[3,8],sit_disturbance_event_pars:3,sit_disturbance_typ:[3,8],sit_disturbance_type_pars:3,sit_disturbance_types_pars:3,sit_ev:3,sit_format:3,sit_inventori:[3,8],sit_inventory_pars:3,sit_map:3,sit_pars:3,sit_read:3,sit_transit:3,sit_transition_rule_pars:3,sit_yield:[3,8],sit_yield_pars:3,sitmap:3,size:7,slash:8,slow:0,slow_decay_op:0,slow_mixing_op:0,snag:0,snag_turnover_op:0,softwood:3,softwoodbranchsnag:8,softwoodcoarseroot:8,softwoodfineroot:8,softwoodfoliag:8,softwoodmerch:8,softwoodoth:8,softwoodstemsnag:8,soil:[1,2],solv:3,sort:[3,4],sort_kei:8,sort_typ:3,sourc:[1,3,5],source_pool:[1,6],span:7,spatial:[1,3],spatial_refer:[3,8],spatial_unit:[1,8],spatial_unit_id:1,speci:[1,3,4,8],special:6,species_classifi:8,species_id:[0,1,2],species_map:8,species_nam:1,specif:[0,3],specifi:[0,1,2,3,4,6,7,8],spin:8,spinup:[0,2,4,5],spinup_debug:4,spruce:8,sqlite3:[1,5],sqlite:1,sqlite_path:1,stand:[0,1,2,4,6],stand_index:6,standard:[2,4,5],standardimporttoolplugin:4,start:[0,1,2],start_year:[3,8],state:[0,2,5],state_comparison:4,state_ind:[2,8],state_vari:[0,2,8],state_variable_result:4,step:[0,2,4,5,7,8],storag:[2,4,6,7,8],store:[1,2,4,6,7,8],str:[0,1,2,3,4,6],string:[0,1,2,3,4,6],structur:[1,6],subdirectori:4,substitut:3,substitute_using_age_class_row:3,sum:8,summar:[2,4],summari:4,summarize_diffs_by_identifi:4,support:[2,3,5,7],sys:4,tabl:[1,3,4,6],table_nam:3,target:3,target_typ:3,temp:0,temperatur:[0,1],test:[2,5],test_case_simul:4,than:[3,4],thei:[3,6],therefor:1,thi:[0,1,2,3,4,6,7,8],those:1,through:[0,2,8],time:[2,3,4,5,7],time_since_land_class_chang:8,time_since_last_disturb:8,time_step:4,timeseri:4,timestep:[0,1,2,4,7,8],timestep_data:7,tool:[4,5],toolbox:4,toolbox_path:4,track:[2,6],transform:4,transit:[0,1,5,8],transition_id:1,transition_rul:3,transitions_factori:2,translat:4,triplet:6,tupl:[1,2,3],turnov:0,turnovercoarselitterinput:8,turnoverfinelitterinput:8,turnoverfollitterinput:8,turnovermerchlitterinput:8,turnoverothlitterinput:8,type:[0,1,2,4,5,6,7,8],undefin:3,underli:[1,6,7],unfccc:[1,4],unfccc_fl_r_fl:1,uniqu:6,unit:[1,3],unlimit:4,unpack:7,unpack_column:3,unpack_ndarrai:7,unpack_t:3,unspecifi:[1,4],updat:[0,6],usag:5,use:[1,2,3],used:[0,1,2,3,4,6,7],useful:[5,6],user:[2,5],user_dist_typ:8,user_speci:8,using:[1,2,3,4,5,8],using_age_class:3,v10:8,valid:[2,3,4,6,8],valu:[0,1,2,3,4,6,7],value_col:4,valueerror:[0,1,3,4,6,7],vari:3,variabl:[0,2,4,5,7],variant:6,variou:8,vector:[1,6,7],version:5,versu:4,via:[0,1,4],violat:3,vol0:0,voln:0,volum:[0,2,3,4,5],were:3,when:[0,3,6],where:[1,4,6],wherea:2,whether:3,which:[0,1,2,3,4,6,7,8],whose:7,wildcard:3,wildfir:8,window:[4,5,6],within:[4,6],without:3,word:4,work:[0,1,2,5],would:4,wrap:0,wrapper:[0,1,2,6,7],written:4,x_label:4,y_label:4,year:[1,3,4],yield:[0,5,8],yield_tabl:[3,8],zero:[0,3,6],zip:4},titles:["CBM core functionality","CBM Input and Variables","CBM","CBM Standard Import tool format","CBM testing","libcbm","LibCBM core functionality","Other functions","Standard Import tool Example"],titleterms:{"case":4,"class":[2,3],"default":1,"function":[0,4,6,7],"import":[3,8],Age:3,The:[2,3],appendix:8,cbm:[0,1,2,3,4],cfs3:4,classifi:[1,3],code:5,comparison:4,core:[0,6],curv:1,data:8,demonstr:[],disturb:3,document:5,event:3,exampl:8,featur:5,flux:[1,4,8],format:3,gener:4,growth:3,indic:[5,8],input:[1,3],inventori:[1,3],kei:5,libcbm:[5,6],map:3,merchant:1,other:7,paramet:1,pool:[1,4,8],read:3,refer:1,requir:5,result:8,rule:3,setup:8,simul:[2,3,4,8],sit:[3,8],sourc:8,spinup:1,standard:[3,8],state:[1,4,8],step:1,support:4,tabl:5,test:4,time:1,tool:[3,8],transit:3,type:3,usag:2,variabl:[1,8],volum:1,yield:3}})