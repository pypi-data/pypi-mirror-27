depends = ('ITKPyBase', 'ITKImageIntensity', )
templates = (
  ('BinaryContourImageFilter', 'itk::BinaryContourImageFilter', 'itkBinaryContourImageFilterISS2ISS2', True, 'itk::Image< signed short,2 >, itk::Image< signed short,2 >'),
  ('BinaryContourImageFilter', 'itk::BinaryContourImageFilter', 'itkBinaryContourImageFilterISS3ISS3', True, 'itk::Image< signed short,3 >, itk::Image< signed short,3 >'),
  ('BinaryContourImageFilter', 'itk::BinaryContourImageFilter', 'itkBinaryContourImageFilterIUC2IUC2', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned char,2 >'),
  ('BinaryContourImageFilter', 'itk::BinaryContourImageFilter', 'itkBinaryContourImageFilterIUC3IUC3', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >'),
  ('BinaryContourImageFilter', 'itk::BinaryContourImageFilter', 'itkBinaryContourImageFilterIF2IF2', True, 'itk::Image< float,2 >, itk::Image< float,2 >'),
  ('BinaryContourImageFilter', 'itk::BinaryContourImageFilter', 'itkBinaryContourImageFilterIF3IF3', True, 'itk::Image< float,3 >, itk::Image< float,3 >'),
  ('ChangeLabelImageFilter', 'itk::ChangeLabelImageFilter', 'itkChangeLabelImageFilterIUC2IUC2', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned char,2 >'),
  ('ChangeLabelImageFilter', 'itk::ChangeLabelImageFilter', 'itkChangeLabelImageFilterIUC3IUC3', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >'),
  ('ChangeLabelImageFilter', 'itk::ChangeLabelImageFilter', 'itkChangeLabelImageFilterISS2ISS2', True, 'itk::Image< signed short,2 >, itk::Image< signed short,2 >'),
  ('ChangeLabelImageFilter', 'itk::ChangeLabelImageFilter', 'itkChangeLabelImageFilterISS3ISS3', True, 'itk::Image< signed short,3 >, itk::Image< signed short,3 >'),
  ('LabelContourImageFilter', 'itk::LabelContourImageFilter', 'itkLabelContourImageFilterISS2ISS2', True, 'itk::Image< signed short,2 >, itk::Image< signed short,2 >'),
  ('LabelContourImageFilter', 'itk::LabelContourImageFilter', 'itkLabelContourImageFilterISS3ISS3', True, 'itk::Image< signed short,3 >, itk::Image< signed short,3 >'),
  ('LabelContourImageFilter', 'itk::LabelContourImageFilter', 'itkLabelContourImageFilterIUC2IUC2', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned char,2 >'),
  ('LabelContourImageFilter', 'itk::LabelContourImageFilter', 'itkLabelContourImageFilterIUC3IUC3', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >'),
  ('LabelContourImageFilter', 'itk::LabelContourImageFilter', 'itkLabelContourImageFilterIF2IF2', True, 'itk::Image< float,2 >, itk::Image< float,2 >'),
  ('LabelContourImageFilter', 'itk::LabelContourImageFilter', 'itkLabelContourImageFilterIF3IF3', True, 'itk::Image< float,3 >, itk::Image< float,3 >'),
)
