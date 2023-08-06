depends = ('ITKPyBase', 'ITKCommon', )
templates = (
  ('PyCommand', 'itk::PyCommand', 'itkPyCommand', False),
  ('PyImageFilter', 'itk::PyImageFilter', 'itkPyImageFilterIUC2IUC2', False, 'itk::Image< unsigned char,2 >, itk::Image< unsigned char,2 >'),
  ('PyImageFilter', 'itk::PyImageFilter', 'itkPyImageFilterIUC3IUC3', False, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >'),
)
