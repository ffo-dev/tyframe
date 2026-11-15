import polars as pl
from benchmark.source_classes.models import C100
from tyframe.typed_df.polars.typed_polars import TypedPolarsDataFrame


#### CODE-GEN START
class C100Pl(TypedPolarsDataFrame[C100]):
    model: type[C100] = C100
    c_1: str = 'c_1'
    c_2: str = 'c_2'
    c_3: str = 'c_3'
    c_4: str = 'c_4'
    c_5: str = 'c_5'
    c_6: str = 'c_6'
    c_7: str = 'c_7'
    c_8: str = 'c_8'
    c_9: str = 'c_9'
    c_10: str = 'c_10'
    c_11: str = 'c_11'
    c_12: str = 'c_12'
    c_13: str = 'c_13'
    c_14: str = 'c_14'
    c_15: str = 'c_15'
    c_16: str = 'c_16'
    c_17: str = 'c_17'
    c_18: str = 'c_18'
    c_19: str = 'c_19'
    c_20: str = 'c_20'
    c_21: str = 'c_21'
    c_22: str = 'c_22'
    c_23: str = 'c_23'
    c_24: str = 'c_24'
    c_25: str = 'c_25'
    c_26: str = 'c_26'
    c_27: str = 'c_27'
    c_28: str = 'c_28'
    c_29: str = 'c_29'
    c_30: str = 'c_30'
    c_31: str = 'c_31'
    c_32: str = 'c_32'
    c_33: str = 'c_33'
    c_34: str = 'c_34'
    c_35: str = 'c_35'
    c_36: str = 'c_36'
    c_37: str = 'c_37'
    c_38: str = 'c_38'
    c_39: str = 'c_39'
    c_40: str = 'c_40'
    c_41: str = 'c_41'
    c_42: str = 'c_42'
    c_43: str = 'c_43'
    c_44: str = 'c_44'
    c_45: str = 'c_45'
    c_46: str = 'c_46'
    c_47: str = 'c_47'
    c_48: str = 'c_48'
    c_49: str = 'c_49'
    c_50: str = 'c_50'
    c_51: str = 'c_51'
    c_52: str = 'c_52'
    c_53: str = 'c_53'
    c_54: str = 'c_54'
    c_55: str = 'c_55'
    c_56: str = 'c_56'
    c_57: str = 'c_57'
    c_58: str = 'c_58'
    c_59: str = 'c_59'
    c_60: str = 'c_60'
    c_61: str = 'c_61'
    c_62: str = 'c_62'
    c_63: str = 'c_63'
    c_64: str = 'c_64'
    c_65: str = 'c_65'
    c_66: str = 'c_66'
    c_67: str = 'c_67'
    c_68: str = 'c_68'
    c_69: str = 'c_69'
    c_70: str = 'c_70'
    c_71: str = 'c_71'
    c_72: str = 'c_72'
    c_73: str = 'c_73'
    c_74: str = 'c_74'
    c_75: str = 'c_75'
    c_76: str = 'c_76'
    c_77: str = 'c_77'
    c_78: str = 'c_78'
    c_79: str = 'c_79'
    c_80: str = 'c_80'
    c_81: str = 'c_81'
    c_82: str = 'c_82'
    c_83: str = 'c_83'
    c_84: str = 'c_84'
    c_85: str = 'c_85'
    c_86: str = 'c_86'
    c_87: str = 'c_87'
    c_88: str = 'c_88'
    c_89: str = 'c_89'
    c_90: str = 'c_90'
    c_91: str = 'c_91'
    c_92: str = 'c_92'
    c_93: str = 'c_93'
    c_94: str = 'c_94'
    c_95: str = 'c_95'
    c_96: str = 'c_96'
    c_97: str = 'c_97'
    c_98: str = 'c_98'
    c_99: str = 'c_99'
    c_100: str = 'c_100'

    @property
    def c_1_col(self) -> pl.Series:
        return self._df[self.c_1]

    @property
    def c_2_col(self) -> pl.Series:
        return self._df[self.c_2]

    @property
    def c_3_col(self) -> pl.Series:
        return self._df[self.c_3]

    @property
    def c_4_col(self) -> pl.Series:
        return self._df[self.c_4]

    @property
    def c_5_col(self) -> pl.Series:
        return self._df[self.c_5]

    @property
    def c_6_col(self) -> pl.Series:
        return self._df[self.c_6]

    @property
    def c_7_col(self) -> pl.Series:
        return self._df[self.c_7]

    @property
    def c_8_col(self) -> pl.Series:
        return self._df[self.c_8]

    @property
    def c_9_col(self) -> pl.Series:
        return self._df[self.c_9]

    @property
    def c_10_col(self) -> pl.Series:
        return self._df[self.c_10]

    @property
    def c_11_col(self) -> pl.Series:
        return self._df[self.c_11]

    @property
    def c_12_col(self) -> pl.Series:
        return self._df[self.c_12]

    @property
    def c_13_col(self) -> pl.Series:
        return self._df[self.c_13]

    @property
    def c_14_col(self) -> pl.Series:
        return self._df[self.c_14]

    @property
    def c_15_col(self) -> pl.Series:
        return self._df[self.c_15]

    @property
    def c_16_col(self) -> pl.Series:
        return self._df[self.c_16]

    @property
    def c_17_col(self) -> pl.Series:
        return self._df[self.c_17]

    @property
    def c_18_col(self) -> pl.Series:
        return self._df[self.c_18]

    @property
    def c_19_col(self) -> pl.Series:
        return self._df[self.c_19]

    @property
    def c_20_col(self) -> pl.Series:
        return self._df[self.c_20]

    @property
    def c_21_col(self) -> pl.Series:
        return self._df[self.c_21]

    @property
    def c_22_col(self) -> pl.Series:
        return self._df[self.c_22]

    @property
    def c_23_col(self) -> pl.Series:
        return self._df[self.c_23]

    @property
    def c_24_col(self) -> pl.Series:
        return self._df[self.c_24]

    @property
    def c_25_col(self) -> pl.Series:
        return self._df[self.c_25]

    @property
    def c_26_col(self) -> pl.Series:
        return self._df[self.c_26]

    @property
    def c_27_col(self) -> pl.Series:
        return self._df[self.c_27]

    @property
    def c_28_col(self) -> pl.Series:
        return self._df[self.c_28]

    @property
    def c_29_col(self) -> pl.Series:
        return self._df[self.c_29]

    @property
    def c_30_col(self) -> pl.Series:
        return self._df[self.c_30]

    @property
    def c_31_col(self) -> pl.Series:
        return self._df[self.c_31]

    @property
    def c_32_col(self) -> pl.Series:
        return self._df[self.c_32]

    @property
    def c_33_col(self) -> pl.Series:
        return self._df[self.c_33]

    @property
    def c_34_col(self) -> pl.Series:
        return self._df[self.c_34]

    @property
    def c_35_col(self) -> pl.Series:
        return self._df[self.c_35]

    @property
    def c_36_col(self) -> pl.Series:
        return self._df[self.c_36]

    @property
    def c_37_col(self) -> pl.Series:
        return self._df[self.c_37]

    @property
    def c_38_col(self) -> pl.Series:
        return self._df[self.c_38]

    @property
    def c_39_col(self) -> pl.Series:
        return self._df[self.c_39]

    @property
    def c_40_col(self) -> pl.Series:
        return self._df[self.c_40]

    @property
    def c_41_col(self) -> pl.Series:
        return self._df[self.c_41]

    @property
    def c_42_col(self) -> pl.Series:
        return self._df[self.c_42]

    @property
    def c_43_col(self) -> pl.Series:
        return self._df[self.c_43]

    @property
    def c_44_col(self) -> pl.Series:
        return self._df[self.c_44]

    @property
    def c_45_col(self) -> pl.Series:
        return self._df[self.c_45]

    @property
    def c_46_col(self) -> pl.Series:
        return self._df[self.c_46]

    @property
    def c_47_col(self) -> pl.Series:
        return self._df[self.c_47]

    @property
    def c_48_col(self) -> pl.Series:
        return self._df[self.c_48]

    @property
    def c_49_col(self) -> pl.Series:
        return self._df[self.c_49]

    @property
    def c_50_col(self) -> pl.Series:
        return self._df[self.c_50]

    @property
    def c_51_col(self) -> pl.Series:
        return self._df[self.c_51]

    @property
    def c_52_col(self) -> pl.Series:
        return self._df[self.c_52]

    @property
    def c_53_col(self) -> pl.Series:
        return self._df[self.c_53]

    @property
    def c_54_col(self) -> pl.Series:
        return self._df[self.c_54]

    @property
    def c_55_col(self) -> pl.Series:
        return self._df[self.c_55]

    @property
    def c_56_col(self) -> pl.Series:
        return self._df[self.c_56]

    @property
    def c_57_col(self) -> pl.Series:
        return self._df[self.c_57]

    @property
    def c_58_col(self) -> pl.Series:
        return self._df[self.c_58]

    @property
    def c_59_col(self) -> pl.Series:
        return self._df[self.c_59]

    @property
    def c_60_col(self) -> pl.Series:
        return self._df[self.c_60]

    @property
    def c_61_col(self) -> pl.Series:
        return self._df[self.c_61]

    @property
    def c_62_col(self) -> pl.Series:
        return self._df[self.c_62]

    @property
    def c_63_col(self) -> pl.Series:
        return self._df[self.c_63]

    @property
    def c_64_col(self) -> pl.Series:
        return self._df[self.c_64]

    @property
    def c_65_col(self) -> pl.Series:
        return self._df[self.c_65]

    @property
    def c_66_col(self) -> pl.Series:
        return self._df[self.c_66]

    @property
    def c_67_col(self) -> pl.Series:
        return self._df[self.c_67]

    @property
    def c_68_col(self) -> pl.Series:
        return self._df[self.c_68]

    @property
    def c_69_col(self) -> pl.Series:
        return self._df[self.c_69]

    @property
    def c_70_col(self) -> pl.Series:
        return self._df[self.c_70]

    @property
    def c_71_col(self) -> pl.Series:
        return self._df[self.c_71]

    @property
    def c_72_col(self) -> pl.Series:
        return self._df[self.c_72]

    @property
    def c_73_col(self) -> pl.Series:
        return self._df[self.c_73]

    @property
    def c_74_col(self) -> pl.Series:
        return self._df[self.c_74]

    @property
    def c_75_col(self) -> pl.Series:
        return self._df[self.c_75]

    @property
    def c_76_col(self) -> pl.Series:
        return self._df[self.c_76]

    @property
    def c_77_col(self) -> pl.Series:
        return self._df[self.c_77]

    @property
    def c_78_col(self) -> pl.Series:
        return self._df[self.c_78]

    @property
    def c_79_col(self) -> pl.Series:
        return self._df[self.c_79]

    @property
    def c_80_col(self) -> pl.Series:
        return self._df[self.c_80]

    @property
    def c_81_col(self) -> pl.Series:
        return self._df[self.c_81]

    @property
    def c_82_col(self) -> pl.Series:
        return self._df[self.c_82]

    @property
    def c_83_col(self) -> pl.Series:
        return self._df[self.c_83]

    @property
    def c_84_col(self) -> pl.Series:
        return self._df[self.c_84]

    @property
    def c_85_col(self) -> pl.Series:
        return self._df[self.c_85]

    @property
    def c_86_col(self) -> pl.Series:
        return self._df[self.c_86]

    @property
    def c_87_col(self) -> pl.Series:
        return self._df[self.c_87]

    @property
    def c_88_col(self) -> pl.Series:
        return self._df[self.c_88]

    @property
    def c_89_col(self) -> pl.Series:
        return self._df[self.c_89]

    @property
    def c_90_col(self) -> pl.Series:
        return self._df[self.c_90]

    @property
    def c_91_col(self) -> pl.Series:
        return self._df[self.c_91]

    @property
    def c_92_col(self) -> pl.Series:
        return self._df[self.c_92]

    @property
    def c_93_col(self) -> pl.Series:
        return self._df[self.c_93]

    @property
    def c_94_col(self) -> pl.Series:
        return self._df[self.c_94]

    @property
    def c_95_col(self) -> pl.Series:
        return self._df[self.c_95]

    @property
    def c_96_col(self) -> pl.Series:
        return self._df[self.c_96]

    @property
    def c_97_col(self) -> pl.Series:
        return self._df[self.c_97]

    @property
    def c_98_col(self) -> pl.Series:
        return self._df[self.c_98]

    @property
    def c_99_col(self) -> pl.Series:
        return self._df[self.c_99]

    @property
    def c_100_col(self) -> pl.Series:
        return self._df[self.c_100]


#### CODE-GEN END
